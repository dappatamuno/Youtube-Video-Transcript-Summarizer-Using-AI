from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from youtube_utils import get_transcript
from embedding_utils import embed_transcript, save_index, load_index
from rag_engine import ask_question
import os
import json

app = FastAPI()
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

class TranscriptRequest(BaseModel):
    youtube_url: str

class QuestionRequest(BaseModel):
    video_id: str
    question: str

@app.post("/transcribe/")
def transcribe_video(request: TranscriptRequest):
    try:
        video_id, transcript, chunks = get_transcript(request.youtube_url)
        index, embeddings = embed_transcript(video_id, chunks)

        index_path = f"{DATA_DIR}/{video_id}.index"
        chunk_path = f"{DATA_DIR}/{video_id}_chunks.json"
        save_index(index, index_path)

        with open(chunk_path, "w") as f:
            json.dump(chunks, f)

        return {"video_id": video_id, "summary": "Transcript successfully embedded."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask/")
def ask(request: QuestionRequest):
    index_path = f"{DATA_DIR}/{request.video_id}.index"
    chunk_path = f"{DATA_DIR}/{request.video_id}_chunks.json"

    if not os.path.exists(index_path) or not os.path.exists(chunk_path):
        raise HTTPException(status_code=404, detail="Video not found. Transcribe it first.")

    index = load_index(index_path)
    with open(chunk_path) as f:
        chunks = json.load(f)

    answer = ask_question(index, chunks, request.question)
    return {"answer": answer}