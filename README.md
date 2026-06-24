# ai-knowledge-assistant
AI-powered knowledge assistant with RAG, document processing, hybrid search, streaming chat, and source citations built using FastAPI, React, PostgreSQL, and Ollama.
# AI Knowledge Assistant

A full-stack AI-powered Knowledge Assistant built with FastAPI, React, PostgreSQL, pgvector, and Ollama.

The application enables users to upload documents, perform semantic search, and chat with an AI assistant using Retrieval-Augmented Generation (RAG). It supports real-time streaming responses, source citations, conversation memory, and hybrid retrieval.

---

## Features

### Authentication

* User Registration
* User Login
* JWT Authentication
* Protected Routes

### AI Chat

* Standard AI Chat
* Chat Session Management
* Conversation History
* Automatic Session Title Generation
* Real-Time Streaming Responses (SSE)

### Retrieval-Augmented Generation (RAG)

* Document-based Question Answering
* Semantic Search using pgvector
* Hybrid Retrieval (Vector Search + Keyword Search)
* Query Rewriting
* Context-Aware Responses
* Source Citations

### Document Management

* Upload Documents
* Drag & Drop Upload
* Processing Status Tracking
* Delete Documents
* Background Document Processing

### Search

* Search Uploaded Documents
* View Relevant Chunks
* Similarity-Based Retrieval

### Conversation Intelligence

* Conversation Memory
* Automatic Conversation Summaries
* Context Preservation Across Sessions

---

## Tech Stack

### Backend

* FastAPI
* PostgreSQL
* pgvector
* SQLAlchemy
* Alembic
* JWT Authentication
* Ollama

### Frontend

* React
* Vite
* React Router
* React Markdown
* CSS

### AI Components

* RAG (Retrieval-Augmented Generation)
* Embeddings
* Hybrid Retrieval
* Query Rewriting
* Conversation Summarization
* Source Citation Generation

---

## Architecture

```text
User
  │
  ▼
React Frontend
  │
  ▼
FastAPI Backend
  │
  ├── Authentication
  ├── Chat Service
  ├── RAG Service
  ├── Document Service
  └── Search Service
  │
  ▼
PostgreSQL + pgvector
  │
  ├── Users
  ├── Sessions
  ├── Messages
  ├── Documents
  └── Vector Embeddings
  │
  ▼
Ollama LLM
```

## Project Structure

```text
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── alembic/
├── requirements.txt
└── main.py


frontend/
│
├── src/
│   ├── api/
│   ├── components/
│   ├── context/
│   ├── pages/
│   ├── styles/
│   └── utils/
│
├── package.json
└── vite.config.js
```

## Key Implementations

* JWT Authentication
* Chat Sessions
* AI Chat
* RAG Chat
* Real-Time Streaming Responses
* pgvector Semantic Search
* Hybrid Retrieval
* Query Rewriting
* Conversation Memory
* Conversation Summarization
* Source Citations
* Document Upload & Processing
* Search Interface
* Responsive UI

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/ai-knowledge-assistant.git

cd ai-knowledge-assistant
```

### Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### PostgreSQL Setup

Enable pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

Run migrations:

```bash
alembic upgrade head
```

Start backend:

```bash
uvicorn app.main:app --reload
```

---

### Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

## Environment Variables

Create a `.env` file inside backend:

```env
DATABASE_URL=postgresql://postgres:password@localhost/ai_assistant

SECRET_KEY=your_secret_key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=60

OLLAMA_BASE_URL=http://localhost:11434

MODEL_NAME=llama3
```

---

## API Features

### Authentication

```http
POST /auth/register
POST /auth/login
```

### Chat

```http
POST /chat/message
POST /chat/message/stream
```

### Sessions

```http
GET /sessions
POST /sessions
```

### Documents

```http
POST /documents/upload
GET /documents
DELETE /documents/{id}
```

### Search

```http
POST /search
```

---

## Future Enhancements

* Multi-LLM Support
* OpenAI Integration
* Gemini Integration
* Chat Rename/Delete
* Analytics Dashboard
* Feedback System
* Docker Deployment
* Kubernetes Deployment
* Team Workspaces
* Role-Based Access Control

---

## Resume Highlights

* Built a production-style AI Knowledge Assistant using FastAPI and React.
* Implemented Retrieval-Augmented Generation (RAG) using PostgreSQL pgvector.
* Developed a document ingestion and semantic search pipeline.
* Added real-time streaming AI responses using Server-Sent Events.
* Designed scalable service-repository architecture.
* Integrated authentication, conversation memory, summarization, and source citations.

---

## License

MIT License
