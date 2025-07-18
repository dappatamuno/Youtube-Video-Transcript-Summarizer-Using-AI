# YouTube Q&A AI App

Ask questions and get concise answers from any YouTube video using embeddings, local language models, and a sleek Svelte frontend.

---

## Features

- Extracts transcripts using YouTubeTranscriptAPI or Whisper (fallback)
- Embeds transcript chunks with `MiniLM` via `sentence-transformers`
- Uses FAISS for fast vector similarity search (RAG)
- Answers generated via `Mistral` (or any Hugging Face text-gen model)
- Persistent vector store with FAISS + local JSON
- Svelte frontend with loading/error states and chat history

---

## Tech Stack

| Layer      | Tool/Library                        |
|------------|-------------------------------------|
| Backend    | FastAPI, FAISS, Transformers        |
| Embeddings | `sentence-transformers` (MiniLM)    |
| LLM        | Mistral-7B-Instruct (local)         |
| Fallback   | Whisper for audio transcription     |
| Frontend   | Svelte + Tailwind (minimal)         |

---

## Getting Started

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload


