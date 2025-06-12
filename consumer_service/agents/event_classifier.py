class EventClassifierAgent:
    async def __call__(self, event):
        event["classification"] = event["event_type"]
        print(f"[EventClassifierAgent] classified: {event['classification']}")
        return event