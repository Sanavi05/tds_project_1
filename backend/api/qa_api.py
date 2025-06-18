# from fastapi import FastAPI, Query
# from pydantic import BaseModel
# import pickle
# import numpy as np
# from sentence_transformers import SentenceTransformer
# from .aipipe_client import query_aipipe
# from sklearn.metrics.pairwise import cosine_similarity

# app = FastAPI(title="TDS Virtual TA")

# import os

# BASE_DIR = os.path.dirname(__file__)
# VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore.pkl")

# with open(VECTORSTORE_PATH, "rb") as f:
#     vectorstore = pickle.load(f)

# texts = vectorstore["texts"]
# embeddings = np.array(vectorstore["embeddings"])

# # Load model for query embedding
# model = SentenceTransformer("all-MiniLM-L6-v2")

# class QueryInput(BaseModel):
#     question: str

# @app.post("/ask")
# def ask_question(input: QueryInput):
#     question = input.question
#     query_embedding = model.encode([question])

#     # Find similar texts using cosine similarity
#     sims = cosine_similarity(query_embedding, embeddings)[0]
#     top_k = 3
#     top_indices = sims.argsort()[-top_k:][::-1]
#     context = "\n\n".join([texts[i] for i in top_indices])

#     # Prepare prompt
#     prompt = f"""Answer this question using the following context.
# If the context is not enough, say "I don't know."

# Question: {question}

# Context:
# {context}

# Answer:"""

#     answer = query_aipipe(prompt)
#     return {
#         "answer": answer.strip(),
#         "links": [f"Similar Topic {i+1}: {texts[i][:80]}..." for i in top_indices.tolist()]
#     }



from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
from contextlib import asynccontextmanager
import numpy as np
from sentence_transformers import SentenceTransformer
from .aipipe_client import query_aipipe
from sklearn.metrics.pairwise import cosine_similarity
import os
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="TDS Virtual TA")

# Add this after app definition
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins — you can restrict to specific domain later
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)


#app = FastAPI(title="TDS Virtual TA")

# Base paths
BASE_DIR = os.path.dirname(__file__)
DISC_VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore.pkl")
COURSE_VECTORSTORE_PATH = os.path.join(BASE_DIR, "vectorstore_course.pkl")

# Load vectorstores
def load_vectorstore(path):
    with open(path, "rb") as f:
        store = pickle.load(f)
    return store["texts"], np.array(store["embeddings"])

texts_disc, embeds_disc = load_vectorstore(DISC_VECTORSTORE_PATH)
texts_course, embeds_course = load_vectorstore(COURSE_VECTORSTORE_PATH)

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

class QueryInput(BaseModel):
    question: str
    image: str = None  # Optional image (base64)

@app.on_event("startup")
def warm_up_model():
    # Force model and vectorstore to load on boot (not on first request)
    _ = model.encode(["startup check"])


@app.get("/")
def read_root():
    return {"message": "TDS Virtual TA is running!"}


@app.post("/ask")
def ask_question(input: QueryInput):
    question = input.question
    image_b64 = input.image

    query_embedding = model.encode([question])[0]

    def get_top_k(texts, embeddings, k=5):
        sims = cosine_similarity([query_embedding], embeddings)[0]
        indices = sims.argsort()[-k:][::-1]
        return [(texts[i], sims[i]) for i in indices]

    # Top 5 from both sources
    top_disc = get_top_k(texts_disc, embeds_disc, k=3)
    top_course = get_top_k(texts_course, embeds_course, k=3)

    # Combine context
    combined_context = "\n\n".join([text for text, _ in top_disc + top_course])

    # Prompt for AI Pipe
    prompt = f"""Answer this question using the following context.
If the context is not enough, say "I don't know."

Question: {question}

Context:
{combined_context}

Answer:"""

    try:
        answer = query_aipipe(prompt, image=image_b64)
        return {
            "answer": answer.strip(),
            "links": [
                {"url": "https://discourse.onlinedegree.iitm.ac.in", "text": text[:80] + "..."}
                for text, _ in top_disc
            ] + [
                {"url": "https://tds.s-anand.net/#/2025-01", "text": text[:80] + "..."}
                for text, _ in top_course
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
