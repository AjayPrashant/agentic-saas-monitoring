from mlflow_tracking.mlflow_client import log_feedback

class FeedbackLoopAgent:
    async def __call__(self, event):
        # Copy event to avoid mutation
        event = event.copy()

        # Default feedback = 0 (not reviewed yet)
        event["feedback_score"] = 0

        # Log to MLFlow
        log_feedback(
            event_id=event["event_id"],
            feedback_score=event["feedback_score"]
        )

        # Logging
        print(f"[FeedbackLoopAgent] Logged feedback for event {event['event_id']} → score = {event['feedback_score']}")

        return event
