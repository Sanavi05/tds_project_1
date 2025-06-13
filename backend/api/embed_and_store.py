import json
import pickle
from sentence_transformers import SentenceTransformer

# STEP 1: Load original JSON
with open("api/discourse_posts.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# STEP 2: Extract just the topic list
topics = raw_data.get("topic_list", {}).get("topics", [])

# STEP 3: Convert to clean format with title + excerpt
docs = []
for topic in topics:
    title = topic.get("title", "")
    excerpt = topic.get("excerpt", "")
    if title or excerpt:
        docs.append(f"{title.strip()} {excerpt.strip()}")

# STEP 4: Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# STEP 5: Encode
doc_embeddings = model.encode(docs)

# STEP 6: Save to disk
with open("api/vectorstore.pkl", "wb") as f:
    pickle.dump({"texts": docs, "embeddings": doc_embeddings}, f)

print(f"✅ Stored {len(docs)} discourse topic embeddings.")
