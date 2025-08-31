# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

# Load environment variables from .env file
load_dotenv()

# --- 1. Global Components Setup ---

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Initialize Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Initialize Neo4j Graph
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

# --- 2. LangChain Workflow Definition ---

# Retriever Chain: The original GraphCypherQAChain
retriever_chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    allow_dangerous_requests=True
)

# Answer Synthesizer Chain
prompt_template = PromptTemplate.from_template(
    """You are an AI assistant that converts structured JSON data into a natural language answer.
    You will be given a user's question and a JSON object containing the data retrieved from a knowledge graph to answer that question.
    Your task is to analyze the JSON data and formulate a concise, conversational answer that directly addresses the original question.
    Base your answer ONLY on the provided data. Do not make up information.
    Original Question: {question}
    Retrieved Data (JSON): {context}
    Natural Language Answer:"""
)
answer_chain = prompt_template | llm

# Processing Function: Handles the logic between the two chains
def process_retrieval_result(retriever_output):
    question = retriever_output["query"]
    intermediate_steps = retriever_output.get("intermediate_steps", [])
    generated_query = intermediate_steps[0].get("query", "")
    context = intermediate_steps[1].get("context", [])

    if context:
        final_answer_obj = answer_chain.invoke({
            "question": question,
            "context": context
        })
        final_answer = final_answer_obj.content if hasattr(final_answer_obj, 'content') else str(final_answer_obj)
    else:
        final_answer = "I was unable to find an answer to your question in the database."

    return {
        "answer": final_answer,
        "generated_query": generated_query,
        "retrieved_data": context
    }

# Master Chain: The final, unified workflow
master_chain = retriever_chain | RunnableLambda(process_retrieval_result)


# --- 3. Flask API Endpoint ---

@app.route('/api/generate-query', methods=['POST'])
def generate_query():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Question not provided"}), 400

    try:
        # Invoke the master chain with the user's question
        result = master_chain.invoke({"query": question})
        return jsonify(result)

    except Exception as e:
        print(f"Error during master chain invocation: {e}")
        return jsonify({"error": "Failed to process request. See server logs."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)