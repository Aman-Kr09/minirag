# Mini RAG Application

A full-stack RAG (Retrieval-Augmented Generation) application built with **FastAPI** (Python) and **React** (Vite).

## Features

- **Ingestion**: Upload text files or paste text directly. 
- **Chunking**: Recursive character chunking (1000 tokens, 150 overlap).
- **Embeddings**: Uses OpenAI (`text-embedding-3-small`) or Google Gemini (`text-embedding-004`).
- **Vector DB**: Pinecone (Serverless) for storage and retrieval.
- **Reranking**: Optional Reranking step using Cohere (`rerank-english-v3.0`).
- **LLM**: Answer generation with citations using OpenAI (`gpt-4o-mini`) or Gemini Flash.
- **Frontend**: Premium, responsive UI with dark mode and glassmorphism.

## Architecture

1. **Frontend**: React + Vite + Framer Motion (Animations) + Lucide (Icons).
2. **Backend**: FastAPI.
3. **Storage**: Pinecone (Vector Search).

## Setup & Run

### Prerequisites
- Python 3.9+
- Node.js 16+
- API Keys for: Pinecone, OpenAI (or Gemini), and optionally Cohere.

### 1. Backend Setup

```bash
cd backend
python -m venv venv
# Windows
.\venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

pip install -r requirements.txt
```

**Environment Variables:**
Rename `.env.example` to `.env` and fill in your keys:
```
PINECONE_API_KEY=...
PINECONE_INDEX_NAME=mini-rag-index
OPENAI_API_KEY=... 
# OR use GEMINI_API_KEY=...
COHERE_API_KEY=... (Optional, for reranking)
```

**Start Server:**
```bash
python main.py
# Server runs on http://localhost:8000
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
# App runs on http://localhost:5173
```

## Deployment Guide

### Backend (Render/Railway/Fly.io)
1. Push code to GitHub.
2. Link repository to hosting provider.
3. Set Environment Variables in the provider's dashboard.
4. Update `start` command to `uvicorn main:app --host 0.0.0.0 --port $PORT`.

### Frontend (Vercel/Netlify)
1. Push code to GitHub.
2. Import `frontend` directory in Vercel.
3. **Important**: Add Environment Variable `VITE_API_URL` if you change the backend URL (you may need to update `api.js` to read from env vars).

## Trade-offs & Remarks
- **Ingestion Speed**: Currently runs synchronously; for larger files, a background task queue (Celery/BullMQ) would be better.
- **Duplicate Handling**: Basic unique ID generation; robust deduplication is not implemented.
- **Security**: Basic CORS allows all origins (*). In production, restrict this to the frontend domain.
