# app.py (Corrected Agentic Workflow)
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# --- LangChain Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain.tools import Tool
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate

# Load environment variables from .env file
load_dotenv()

# --- 1. Global Components Setup ---

app = Flask(__name__)
CORS(app)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

try:
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI"),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD")
    )
    graph.refresh_schema()
except Exception as e:
    print(f"Error connecting to Neo4j: {e}")
    graph = None

# --- 2. LangChain Agentic Workflow Definition ---

# The tool is now ONLY the data retrieval chain.
graph_qa_chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    allow_dangerous_requests=True
)

tool_description = (
    "This tool is an expert at querying a Neo4j graph database containing information about basketball players, coaches, and teams. "
    "Use it to answer specific, factual questions about PLAYER, COACH, and TEAM nodes and their relationships like TEAMMATES, COACHES, and PLAYS_FOR. "
    "The input to this tool should be a single, clear question that can likely be answered with a single database query. "
    "For example: 'Who is the coach for the LA Lakers?' or 'How many points did LeBron James score against the Memphis Grizzlies?'"
)

tools = [
    Tool(
        name="graph_database_query_tool",
        func=graph_qa_chain.invoke,
        description=tool_description,
    )
]

# CORRECTED PROMPT using a single string template
AGENT_PROMPT_TEMPLATE = """
You are an expert sports analyst and a master planner. Your primary goal is to answer a user's complex question by breaking it down into a series of smaller, factual sub-questions.

**Tools Available:**
You have access to the following tools:
{tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

**Operational Procedure:**
1.  Carefully analyze the user's original question to understand what information is needed.
2.  Formulate the first simple, factual sub-question and use the 'graph_database_query_tool' to find the answer.
3.  Observe the result and repeat the process until you have all the facts to answer the original question.
4.  Synthesize the gathered facts into a final, comprehensive answer.

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

# CORRECTED PROMPT CREATION using the standard PromptTemplate
agent_prompt = PromptTemplate.from_template(AGENT_PROMPT_TEMPLATE)

agent = create_react_agent(llm, tools, agent_prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)

# --- 3. Flask API Endpoint ---

@app.route('/api/generate-query', methods=['POST'])
def generate_query():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"error": "Question not provided"}), 400
    try:
        response = agent_executor.invoke({"input": question})
        return jsonify({"answer": response.get("output")})
    except Exception as e:
        print(f"Error during agent executor invocation: {e}")
        return jsonify({"error": "Failed to process request. See server logs."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)