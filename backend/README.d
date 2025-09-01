# Neo4j Agentic Chatbot API 🤖🧠

This project is a Python-based backend API for a conversational AI chatbot. It leverages a powerful **LangChain agent** to answer complex questions by querying a Neo4j graph database containing NBA player, team, and coach information.

This is not a simple question-answering workflow; it's a true agentic system that can reason, decompose problems, and use multiple tools to arrive at a comprehensive answer.

---
## Core Features

* **Natural Language Interface**: Translates user questions in plain English into precise database queries.
* **Agentic Reasoning**: Utilizes a ReAct (Reason + Act) agent that can break down complex, multi-hop questions into a series of simpler, solvable steps.
* **Multi-Tool Capability**: The agent is equipped with a set of tools to perform its tasks:
    * A **Graph Database Tool** for querying information about players, teams, and their relationships.
    * A **Calculator Tool** for performing mathematical calculations.
* **Detailed Tracing**: The API returns the agent's final answer along with a complete, step-by-step log of its thought process, the tools it used, and the data it observed.

---
## The Agentic Architecture

Unlike a standard RAG (Retrieval-Augmented Generation) workflow that might perform a single query for a single question, this application uses a more advanced **agentic architecture**.

The core of the system is a **planner agent**. When it receives a complex question like *"What is the age difference between Luka Doncic and LeBron James?"*, it doesn't try to answer it in one go. Instead, it operates in a loop:

1.  **Thought**: The agent analyzes the goal and formulates a plan. *(e.g., "I need to find the age of both players first, then calculate the difference.")*
2.  **Action**: The agent decides which tool is best for the next step and formulates a simple input for it. *(e.g., Use the `graph_database_query_tool` with the input "How old is Luka Doncic?")*
3.  **Observation**: The agent executes the tool and receives the factual result. *(e.g., The tool returns that Luka Doncic is 26.)*
4.  **Repeat**: The agent adds this new fact to its "scratchpad" and loops back to the **Thought** step, using its accumulated knowledge to decide what to do next. *(e.g., "Okay, I have Luka's age. Now I need LeBron's age.")*

This reasoning loop continues until the agent has gathered all the necessary facts. Only then does it synthesize them into a final, comprehensive answer. This allows the system to solve problems that would be impossible for a simpler, single-step chain.

---
## Technology Stack

* **Backend Framework**: Python 3.10+ with Flask
* **AI Orchestration**: LangChain (specifically `AgentExecutor` and `GraphCypherQAChain`)
* **Large Language Model**: Google Gemini (`gemini-1.5-flash`)
* **Database**: Neo4j Graph Database

---
## 🚀 Setup and Installation

Follow these steps to get the backend running locally.

**1. Clone the Repository**
```bash
git clone <your-repo-url>
cd <your-repo-name>/backend

# Setup and API Instructions

## 2. Create and Activate a Virtual Environment

### On macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### On Windows:

```bash
python -m venv venv
.\venv\Scripts\activate
```

## 3. Install Dependencies

This project uses a requirements.txt file to manage its dependencies.

```bash
pip install -r requirements.txt
```

## 4. Set Up Environment Variables

Create a file named `.env` in the backend directory. This file will store your secret keys and credentials.

```env
NEO4J_URI="neo4j+s://your-neo4j-aura-uri.databases.neo4j.io"
NEO4J_USERNAME="neo4j"
NEO4J_PASSWORD="your-neo4j-password"
GOOGLE_API_KEY="your-google-ai-api-key"
```

## How to Run

Once the setup is complete, start the Flask development server with the following command:

```bash
python app.py
```

The API will be available at `http://127.0.0.1:5000`.

## API Endpoint

The application exposes a single API endpoint.

### POST /api/generate-query

This endpoint is the main entry point for the chatbot.

**Request Body:**

```json
{
  "question": "Your natural language question here"
}
```

**Success Response (200):**
Returns a detailed JSON object containing the final answer and the agent's step-by-step reasoning.

```json
{
  "input": "The original question",
  "output": "The agent's final natural language answer.",
  "intermediate_steps": [
    {
      "action": {
        "tool": "The name of the tool used",
        "tool_input": "The input given to the tool",
        "log": "The agent's 'Thought' process as a string"
      },
      "observation": "The result returned by the tool"
    }
    // ... more steps ...
  ]
}
```