from llm_integration.ollama_client import generate_summary

class LLMExplainabilityAgent:
    async def __call__(self, event):
        # Copy event to avoid mutation across runs
        event = event.copy()

        if not event.get("is_anomaly"):
            return event

        rag_notes = event.get("rag_notes", [])
        prompt = (
            f"Given the following SaaS event:\n\n"
            f"Event ID: {event['event_id']}\n"
            f"Event Type: {event['event_type']}\n"
            f"User ID: {event['user_id']}\n"
            f"Anomaly Score: {event['anomaly_score']:.2f}\n"
            f"RAG Notes: {rag_notes}\n\n"
            f"Generate a short summary explaining why this event may be risky or anomalous, for the engineering team:"
        )

        summary = generate_summary(prompt)
        event["llm_summary"] = summary
        print(f"[LLMExplainabilityAgent] Summary: {summary}")

        return event
