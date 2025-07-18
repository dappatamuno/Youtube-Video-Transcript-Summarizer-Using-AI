from transformers import pipeline
import numpy as np
from sentence_transformers import SentenceTransformer

qa_model = pipeline("text-generation", model="mistralai/Mistral-7B-Instruct-v0.1", device=-1)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def ask_question(index, chunks, question, top_k=3):
    q_embedding = embedder.encode([question])
    D, I = index.search(np.array(q_embedding), top_k)

    relevant_chunks = [chunks[i] for i in I[0]]
    context = "\n".join(relevant_chunks)

    prompt = f"""
Answer this question based ONLY on the transcript below.
Transcript:
{context}

Question: {question}
Answer concisely in 1-3 sentences.
"""

    output = qa_model(prompt, max_new_tokens=150)[0]["generated_text"]
    return output.split("Answer:")[-1].strip()