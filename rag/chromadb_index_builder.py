import json
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Load KB
with open("data/kb.json", "r") as f:
    kb = json.load(f)

# Setup ChromaDB client
client = chromadb.PersistentClient(path="./rag/chroma_db")
collection = client.get_or_create_collection(name="agent_kb")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Insert embeddings with metadata
for entry in kb:
    text = entry["text"]
    # For this example — I'll infer event type from text:
    if "subscription" in text:
        event_type = "subscription_cancellation"
    elif "login" in text:
        event_type = "user_login"
    elif "500_INTERNAL" in text:
        event_type = "error"
    elif "404_NOT_FOUND" in text:
        event_type = "error"
    elif "payment" in text:
        event_type = "billing_failure"
    elif "support ticket" in text:
        event_type = "support_ticket"
    else:
        event_type = "generic"

    # Add to collection
    collection.add(
        documents=[text],
        metadatas=[{"event_type": event_type}],
        ids=[entry["id"]]
    )

print(f"[ChromaDB] Indexed {len(kb)} KB entries with metadata.")
