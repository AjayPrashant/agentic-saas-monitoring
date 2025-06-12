import chromadb
from sentence_transformers import SentenceTransformer

class RAGAgent:
    def __init__(self, n_results=5, score_threshold=0.3):
        self.n_results = n_results
        self.score_threshold = score_threshold

    async def __call__(self, event):
        # Copy event to avoid cross-event leakage
        event = event.copy()

        if not event.get("is_anomaly"):
            return event

        # Per-call ChromaDB client
        client = chromadb.PersistentClient(path="./rag/chroma_db")
        collection = client.get_or_create_collection(name="agent_kb")

        # Load embedding model (cached after first load)
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # Build query
        query_text = f"{event['event_type']} {event['metadata'].get('error_code','')} user {event['user_id']}"

        # Perform query with metadata filter
        results = collection.query(
            query_texts=[query_text],
            n_results=self.n_results,
            where={"event_type": event["event_type"]}
        )

        raw_notes = results["documents"][0]
        raw_scores = results["distances"][0]

        # Filter by score threshold
        filtered_notes = [
            note for note, score in zip(raw_notes, raw_scores) if score < self.score_threshold
        ]

        # Fallback if no good notes
        if not filtered_notes and raw_notes:
            filtered_notes = [raw_notes[0]]

        event["rag_notes"] = filtered_notes

        # Logging
        print(f"[RAGAgent - Optimized+Metadata] Query: {query_text} (event_type={event['event_type']}) → Notes: {filtered_notes}")

        return event
