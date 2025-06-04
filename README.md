# Hotel Booking Management System (Python, LLM-Powered)

This project is an AI-powered Hotel Booking Management System that leverages LLMs (Large Language Models) to interact with a PostgreSQL database using natural language queries. It provides a FastAPI backend for query handling and a Streamlit demo frontend for user interaction.

## Features

- **Natural Language SQL Agent:** Ask questions about hotel bookings, rooms, users, and more in plain English.
- **LLM Integration:** Uses Groq's Llama-3.3-70b-versatile model via LangChain for intelligent query generation and response.
- **PostgreSQL Database:** Securely connects and queries your hotel management data.
- **FastAPI Backend:** Exposes a `/generate` endpoint for LLM-powered responses.
- **Environment Variable Support:** Securely manage API keys and database credentials.

## Project Structure

```
.
├── src/
│   ├── api/
│   │   ├── agent_api.py         # FastAPI backend with LLM agent
│   │   └── requirements.txt     # Backend dependencies
│   ├── sql_query_agent.ipynb    # Jupyter notebook for development/testing
│   └── ...
├── __init__.py                  # Example usage of the deployed API
├── pyproject.toml               # Project metadata and dependencies
├── dockerfile                   # Docker support
└── README.md                    # Project documentation
```

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hotel-booking-management-system-python.git

cd hotel-booking-management-system-python
```

### 2. Install Dependencies

You can use either `pip` with the provided requirements or a tool like `uv` with `pyproject.toml`.

#### Using pip

```bash
pip install -r src/api/requirements.txt
```

#### Or using uv/poetry

```bash
uv pip install -r src/api/requirements.txt
```

### 3. Set Up Environment Variables

Create a `.env` file in the project root with the following variables:

```
LANGCHAIN_API_KEY=your_langchain_api_key
DATABASE_URL=your_postgresql_database_url
```

### 4. Run the FastAPI Backend

```bash
cd src/api
uvicorn agent_api:app --reload
```

This will launch the FastAPI backend. You can test it by sending a POST request to `http://127.0.0.1:8000/generate` using Postman, curl.

## API Usage

- **POST** `/generate`
  - **Body:** `{ "query": "How many rooms are available?" }`
  - **Response:** Natural language answer from the LLM, based on your database.

## Example

```python
import requests

api_url = "http://127.0.0.1:8000/generate" # if it is local
response = requests.post(api_url, json={"query": "Which room is good for single person?"})
print(response.json())
```

## Development & Testing

- Use `src/sql_query_agent.ipynb` for interactive development and testing of the LLM agent and SQL queries.
- The backend is CORS-enabled for `https://ai-assistant-chatbot-xnhx.onrender.com/generate`.

## Dependencies

- Python 3.12+
- FastAPI
- Uvicorn
- LangChain, LangGraph, LangChain-Groq, LangChain-Community
- Groq API
- psycopg2
- python-dotenv

See `src/api/requirements.txt` or `pyproject.toml` for the full list.

## Docker

A `dockerfile` is provided for containerized deployment.

```
docker pull yebhonelin102273442/hotel-booking:latest
```
