import os
import pickle
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Directory with your 110 .txt files
COURSE_DIR = "backend/data/tds_course_dynamic"

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load and prepare docs
docs = []
filepaths = []

for filename in os.listdir(COURSE_DIR):
    if filename.endswith(".txt"):
        path = os.path.join(COURSE_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()
            if text:
                docs.append(text)
                filepaths.append(path)

# Generate embeddings
print(f"📚 Embedding {len(docs)} course content sections...")
doc_embeddings = model.encode(docs)

# Save embeddings
with open("backend/api/vectorstore_course.pkl", "wb") as f:
    pickle.dump({"texts": docs, "embeddings": doc_embeddings, "files": filepaths}, f)

print(f"✅ Saved course embeddings to vectorstore_course.pkl")
