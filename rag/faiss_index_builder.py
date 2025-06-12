import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load KB
with open("data/kb.json", "r") as f:
    kb = json.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")  # small & fast

# Embed all KB entries
texts = [entry["text"] for entry in kb]
embeddings = model.encode(texts, convert_to_numpy=True)

# Build FAISS index
dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)

# Save artifacts
faiss.write_index(index, "rag/faiss_index.index")
with open("rag/kb_texts.json", "w") as f:
    json.dump(texts, f)

print(f"[FAISS] Indexed {len(texts)} KB entries.")
