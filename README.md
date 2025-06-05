# PDF RAG System

This repository contains a system for processing PDFs using LlamaIndex and Ollama to create a searchable knowledge base. The system allows for quick retrieval and querying of information from your technical documentation.

## Prerequisites

- Nvidia Jetson Nano
- Docker and Docker Compose installed
- PDF documents to process

## Quick Start with Docker

1. Clone this repository:
```bash
git clone https://github.com/TheSamE03/jetson-rag-pipeline.git
cd jetson-rag-pipeline
```

2. Place your PDF documents in the `docs` folder.

3. Start the services using Docker Compose. On Jetson devices the services
   require the `nvidia` container runtime, which is already configured in
   `docker-compose.yml`:
```bash
docker compose up -d
```

### NVIDIA runtime setup (Jetson)
If you see an "unknown or invalid runtime name: nvidia" error, the NVIDIA
container runtime may not be registered with Docker. Create or update
`/etc/docker/daemon.json` as follows and then restart Docker:

```json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  }
}
```

```bash
sudo systemctl restart docker
```

4. Pull the LLM model (first time only):
```bash
curl http://localhost:11434/api/pull -d '{"name": "llama3.2:3b"}'
```

5. The system will be available at:
   - Web UI: http://localhost:3000
   - API: http://localhost:8000

## Components

### 1. Web Interface
The system includes a modern, responsive web interface built with React and Tailwind CSS. Features include:
- Clean, intuitive query interface
- Real-time responses with loading states
- Markdown rendering for formatted answers
- Document source display
- Mobile-responsive design

### 2. Backend API
RESTful API endpoints:
- `POST /query`: Submit questions to the RAG system
- `GET /health`: Check system health

### 3. RAG Engine
- PDF document processing
- Vector storage for efficient retrieval
- Integration with Ollama LLM
- Contextual answer generation

## Manual Setup (without Docker)

If you prefer to run without Docker, follow these steps:

1. Create a virtual environment and activate it:
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running and you have your preferred model downloaded:
```bash
ollama pull llama3.2:3b
```

4. Place your PDF documents in the `docs` folder.

5. For the frontend (optional):
```bash
cd frontend
npm install
npm start
```

## Usage

1. First, index your documents:
```bash
# With Docker:
docker compose exec rag-api python src/index_docs.py

# Without Docker:
python src/index_docs.py
```

2. Access the system:
   - Open your web browser and navigate to `http://localhost:3000`
   - Type your question in the text area
   - Click "Ask Question"
   - View the answer and relevant document snippets

## API Usage

You can also use the API directly:

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"text": "your question here", "num_docs": 3}'
```

Response format:
```json
{
  "answer": "Generated answer...",
  "relevant_docs": [
    "Snippet from document 1...",
    "Snippet from document 2...",
    "Snippet from document 3..."
  ]
}
```

## Configuration

Environment variables (can be set in docker-compose.yml):
```
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3.2:3b
```

## Docker Volumes

- `./docs`: Mount point for your PDF documents
- `./data`: Persistent storage for the vector index
- `ollama_data`: Persistent storage for Ollama models
