# test_connection.py
import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph

# Load environment variables from .env file
load_dotenv()
print("Attempting to connect to Neo4j...")

# Get credentials from environment
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Print the credentials to verify they are loaded (optional, remove password in a real app)
print(f"  URI: {NEO4J_URI}")
print(f"  Username: {NEO4J_USERNAME}")

try:
    # Initialize the Neo4j graph connection
    graph = Neo4jGraph(
        url=NEO4J_URI,
        username=NEO4J_USERNAME,
        password=NEO4J_PASSWORD
    )

    # This is the command that fetches the schema
    graph.refresh_schema()

    print("\n✅ SUCCESS: Connection established and schema was fetched.")
    print("\n--- DATABASE SCHEMA ---")
    print(graph.schema)
    print("-----------------------\n")

except Exception as e:
    print(f"\n❌ FAILURE: Could not connect to the database or fetch schema.")
    print(f"  Error details: {e}\n")