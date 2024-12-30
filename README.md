# Multi-Agent
![picture](https://raw.githubusercontent.com/awslabs/multi-agent-orchestrator/main/img/flow.jpg)

## Introduction

This repository contains an implementation of agentic patterns such as **Planning (ReAct flow)**, **Reflection**, and **Multi-Agent** workflows. It showcases advanced agent orchestration with APIs and tools.

- Follow this repo to learn more about multi-agent patterns: [agentic_patterns](https://github.com/neural-maze/agentic_patterns/)
- Follow this repo to learn more about multi-agent orchestrator: [multi-agent-orchestrator](https://github.com/awslabs/multi-agent-orchestrator)

---

## Project Structure

```plaintext
multi-agent/
│
├── api/                     # API logic
│   ├── routers/             # API routers
│   └── services/            # Service logic
│       └── agent.py         # Main agent services
│
├── docker/                  # Docker setup
│   ├── Dockerfile.backend   # Backend Dockerfile
│   └── Dockerfile.frontend  # Frontend Dockerfile
│
├── src/                     # Source code
│   ├── agents/              # Agent-specific implementations
│   └── tests/               # Test files
│       ├── agent_test.py    # Tests for agents
│       └── llm_test.py      # Tests for LLM functions
│
├── tools/                   # Utility tools
├── utils/                   # Configuration and helper functions
│   ├── config.py            # Configuration settings
│   └── prompt.py            # Prompt definitions
│
├── venv/                    # Virtual environment
├── app_fastapi.py           # FastAPI app
├── app_streamlit.py         # Streamlit app for UI
├── docker-compose.yaml      # Docker Compose setup
├── .env.example             # Environment variable template
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/buithanhdam/multi-agent.git
cd multi-agent
```

### 2. Create and activate a virtual environment (Optional)

- **For Unix/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
- **For Windows:**
  ```bash
  python -m venv venv
  .\venv\Scripts\activate
  ```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Setup Environment Variables

Copy the `.env.example` file to a new `.env` file and update the API keys:

```bash
cp .env.example .env
```

Add the following keys:

```plaintext
GOOGLE_API_KEY=your_google_api_key
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
```

---

## Testing

- Run the test suite using `pytest`:

```bash
pytest src/tests/
```

- Or if you dont want to use `pytest` then run `python` cmd:

```bash
python3 src/tests/llm_test.py
```

```bash
python3 src/tests/agent_test.py
```

---

## Running the Application

### 1. Run FastAPI Backend

```bash
uvicorn app_fastapi:app --host 0.0.0.0 --port 8000 --reload
```

- Access the API at: `http://127.0.0.1:8000`

### 2. Run Streamlit Frontend

```bash
streamlit run app_streamlit.py --server.port=8501 --server.address=0.0.0.0
```

- Access the frontend UI at: `http://localhost:8501`

---

## Run with Docker

### 1. Build Docker Images
- If you dont have `docker-compose` use `docker compose` instead
```bash
docker-compose build
```

### 2. Start Docker Containers

```bash
docker-compose up
```

- The backend will be available at `http://localhost:8000`.
- The frontend will be available at `http://localhost:8501`.

### 3. Stop Docker Containers

To stop the running containers, press `Ctrl+C` or run:

```bash
docker-compose down
```

---

## Contributing

Feel free to open an issue or submit a pull request to improve this project.

---

## License

This project is licensed under the MIT License.

---

## References

- [Agentic Patterns Repo](https://github.com/neural-maze/agentic_patterns/)
- [Multi Agent Orchestrator](https://github.com/awslabs/multi-agent-orchestrator)
