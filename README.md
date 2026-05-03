# Simple-Bot 🤖

A modern chatbot with web search capabilities built using LangGraph, FastAPI, and Streamlit.

## Overview

Simple-Bot is a conversational AI assistant that can:
- Answer questions using LLM capabilities
- Perform real-time web searches to provide up-to-date information
- Run as both a CLI tool and web application
- Deploy easily using Docker

The system implements a **ReAct (Reasoning and Acting)** agent pattern using the LangGraph framework, allowing it to reason about when to use tools and execute them dynamically.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend (8501)                 │
│                       (frontend/ui.py)                       │
└────────────────────────┬──────────────────────────────────────┘
                         │ HTTP Request (POST /chat)
                         ↓
┌─────────────────────────────────────────────────────────────┐
│          FastAPI Backend (8000)        │
│              (backend/app.py)          │
└──────────┬───────────────────
           │
           ↓
┌─────────────────────────────────────────┐
│         LangGraph Agent                 │
│  - LLM: Groq (gpt-oss-120b)            │
│  - Tools: Tavily Web Search             │
└─────────────────────────────────────────┘
```

## Features

- **Dual Interface**: CLI and web-based UI
- **Agent Architecture**: ReAct pattern for reasoning and tool use
- **Web Search Integration**: Real-time information retrieval via Tavily
- **Containerized**: Docker support for easy deployment
- **Conversation Memory**: Threaded conversations with state persistence
- **FastAPI Backend**: Production-ready RESTful API

## Tech Stack

- **Backend**: FastAPI (Python 3.12+)
- **Frontend**: Streamlit
- **AI Framework**: LangGraph, LangChain
- **LLM**: Groq (openai/gpt-oss-120b)
- **Search**: Tavily API
- **Containerization**: Docker & Docker Compose
- **Package Manager**: uv

## Prerequisites

- Python 3.12 or higher
- API keys:
  - GROQ_API_KEY (required)
  - TAVILY_API_KEY (required)
- Docker & Docker Compose (for containerized deployment)
- uv package manager

## Installation

### Option 1: Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Simple-Bot
   ```

2. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

4. **Run the application:**

   **Option A - CLI mode:**
   ```bash
   uv run python backend/main.py
   ```

   **Option B - API + Frontend:**
   ```bash
   # Terminal 1 - Start Backend
   uv run python backend/app.py

   # Terminal 2 - Start Frontend
   uv run streamlit run frontend/ui.py
   ```

### Option 2: Docker Deployment

1. **Configure API keys in `.env`:**
   ```bash
   echo "GROQ_API_KEY=your_key_here" > .env
   echo "TAVILY_API_KEY=your_key_here" >> .env
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Frontend UI: http://localhost:8501
   - Backend API: http://localhost:8000
   - Health Check: http://localhost:8000/health

## Usage

### Web Interface

1. Open http://localhost:8501 in your browser
2. Type your question in the chat input
3. The agent will automatically determine if web search is needed
4. View the response with search citations

### API Endpoint

Send POST requests to `http://localhost:8000/chat`:

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

Response:
```json
{
  "reply": "The capital of France is Paris...",
  "thread_id": "1",
  "status": "success"
}
```

### CLI Mode

For testing and development:

```bash
uv run python backend/main.py
```

Type your queries interactively. Type `exit`, `quit`, or `q` to quit.

## Project Structure

```
Simple-Bot/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── main.py             # CLI entry point
│   └── Dockerfile          # Backend container config
├── frontend/
│   ├── ui.py               # Streamlit UI
│   └── Dockerfile          # Frontend container config
├── src/
│   ├── __init__.py
│   ├── workflow.py         # LangGraph agent workflow
│   ├── tool.py            # Web search tool implementation
│   ├── schema.py          # Data models (Pydantic)
│   └── state.py           # Agent state definition
├── .env                   # Environment variables
├── docker-compose.yml     # Container orchestration
├── pyproject.toml         # Project dependencies
└── README.md             # This file
```

## Agent Workflow

The ReAct agent follows this pattern:

1. **Input**: User message
2. **LLM Call**: Model analyzes message and decides if tools are needed
3. **Tool Execution**: If needed, web search is performed
4. **Response**: Model formulates final answer based on search results
5. **State Management**: Conversation history is maintained per thread

### Tool Integration

**Web Search Tool**: `websearch_tool`
- Input: Search query string
- Output: Top search result content
- Usage: Automatically invoked when LLM determines real-time info is needed

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GROQ_API_KEY` | API key for Groq LLM service | Yes |
| `TAVILY_API_KEY` | API key for Tavily web search | Yes |
| `NVIDIA_API_KEY` | Optional NVIDIA API key | No |
| `OPEN_ROUTER_API_KEY` | Optional OpenRouter API key | No |

### Docker Configuration

The `docker-compose.yml` configures:
- Backend service on port 8000
- Frontend service on port 8501
- Automatic backend URL configuration for frontend
- Health checks and restart policies

## Development

### Project Setup

This project uses `uv` for dependency management:

```bash
# Sync dependencies
uv sync

# Add new packages
uv add <package-name>

# Run with uv
uv run python <script.py>
```

### Code Structure

- **State Management**: Uses LangGraph's StateGraph with AgentState
- **Tools**: Structured tools with Pydantic schemas
- **API**: FastAPI with Pydantic models for request/response
- **Frontend**: Streamlit session state for chat history

### Key Files

- `src/workflow.py`: Core agent logic and graph construction
- `src/tool.py`: Tool definitions and implementations
- `backend/app.py`: FastAPI endpoints and error handling
- `frontend/ui.py`: Streamlit UI and backend communication

## Troubleshooting

### Port Conflicts

If ports are already in use:

```bash
# Change ports in docker-compose.yml
backend:
  ports:
    - "8001:8000"  # Host:Container

frontend:
  ports:
    - "8502:8501"
```

### Connection Issues

Backend not reachable:
- Check backend logs: `docker-compose logs backend`
- Verify backend health: `curl http://localhost:8000/health`
- Check environment variables in `.env`

### API Key Errors

Verify keys are set correctly:
```bash
docker-compose down
docker-compose up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature-name`)
3. Make your changes
4. Test locally (both CLI and Docker modes)
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with [LangGraph](https://langchain-ai.github.io/langgraph/) and [LangChain](https://www.langchain.com/)
- Powered by [Groq](https://groq.com/) and [Tavily](https://tavily.com/)
- Containerized with [Docker](https://www.docker.com/)

---

For more detailed Docker deployment instructions, see [README_DOCKER.md](README_DOCKER.md).
