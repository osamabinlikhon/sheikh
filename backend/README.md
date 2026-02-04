# Agent Sheikh - Backend

This is the backend server for Agent Sheikh, built with FastAPI. It handles agent orchestration, sandbox management, and tool execution.

## Features

- **PlanAct Agent**: Orchestrates task planning and tool execution.
- **Sandbox Management**: Manages Docker-based sandbox environments.
- **LLM Integration**: Integrates with Codestral for intelligent task execution.
- **Tool Registry**: Extensible system for managing agent tools.
- **Async API**: Built on FastAPI for high performance and scalability.

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB (via Motor)
- **Caching**: Redis
- **Containerization**: Docker SDK for Python
- **LLM Client**: HTTPX for Codestral API

## Project Structure

```
backend/
├── app/
│   ├── api/            # API endpoints (auth, chat, sandbox, etc.)
│   ├── core/           # Core logic (agent, llm, tools, sandbox)
│   ├── models/         # Database models
│   ├── schemas/        # Pydantic schemas for validation
│   ├── services/       # Business logic services
│   ├── utils/          # Utility functions
│   ├── config.py       # Configuration management
│   └── main.py         # Application entry point
├── tests/              # Test suite
├── .env.example        # Environment variable template
├── Dockerfile          # Container definition
└── requirements.txt    # Python dependencies
```

## Setup & Installation

### Prerequisites

- Python 3.11+
- MongoDB
- Redis
- Docker (running locally)

### Local Development

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys and configuration
   ```

5. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`.
API documentation can be accessed at `http://localhost:8000/docs`.

## Testing

Run the test suite using `pytest`:

```bash
pytest
```

## Linting and Formatting

We use `black` for formatting and `ruff` for linting:

```bash
# Format code
black .

# Run linting
ruff check .
```
