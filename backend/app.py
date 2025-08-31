# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import GraphCypherQAChain, Neo4jGraph

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# Neo4j and LangChain setup
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize the Neo4j graph connection 
try:
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD
    )
    # Refresh schema to ensure it's up-to-date
    graph.refresh_schema()
except Exception as e:
    print(f"Error connecting to Neo4j: {e}")
    graph = None

# Initialize the Gemini LLM
try:
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
except Exception as e:
    print(f"Error initializing Gemini LLM: {e}")
    llm = None

# Create the LangChain GraphCypherQAChain
if graph and llm:
    try:
        chain = GraphCypherQAChain.from_llm(
            llm=llm,
            graph=graph,
            verbose=True, # Set to True for debugging
            return_intermediate_steps=True, # Crucial for getting the generated query
            allow_dangerous_requests=True  # Add this line to acknowledge the security warning
        )
    except Exception as e:
        print(f"Error creating GraphCypherQAChain: {e}")
        chain = None
else:
    chain = None

@app.route('/api/generate-query', methods=['POST'])
def generate_query():
    if not chain:
        return jsonify({"error": "Backend chain not initialized. Check server logs."}), 500

    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Question not provided"}), 400

    try:
        # Invoke the chain with the user's question
        result = chain.invoke({"query": question})

        # The generated Cypher query is in the intermediate_steps
        generated_query = result['intermediate_steps'][0]['query']

        return jsonify({"cypher_query": generated_query})

    except Exception as e:
        print(f"Error during chain invocation: {e}")
        return jsonify({"error": "Failed to generate query. See server logs for details."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)