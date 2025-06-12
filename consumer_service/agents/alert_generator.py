from slack_integration.slack_client import send_alert
from mlflow_tracking.mlflow_client import log_event_metrics

class AlertGeneratorAgent:
    async def __call__(self, event):
        is_anomaly = event.get("is_anomaly", False)
        anomaly_score = event.get("anomaly_score", 0.0)

        if is_anomaly:
            # Build alert message
            alert_msg = (
                f"🚨 *Anomaly detected!*\n"
                f"Event ID: {event['event_id']}\n"
                f"Type: {event['event_type']}\n"
                f"User: {event['user_id']}\n"
                f"Anomaly Score: {anomaly_score:.2f}"
            )

            # Add RAG notes if present
            rag_notes = event.get("rag_notes", [])
            if rag_notes:
                alert_msg += "\n*RAG Notes:* " + "; ".join(rag_notes)

            # Add LLM summary if present
            llm_summary = event.get("llm_summary", "")
            if llm_summary:
                alert_msg += f"\n*LLM Summary:* {llm_summary}"

            # Print to console
            print(f"[AlertGeneratorAgent] {alert_msg}")

            # Send to Slack
            send_alert(alert_msg)

            alert_triggered = True
        else:
            alert_triggered = False

        # Log to MLFlow
        log_event_metrics(
            event_id=event["event_id"],
            event_type=event["event_type"],
            anomaly_score=anomaly_score,
            is_anomaly=is_anomaly,
            alert_triggered=alert_triggered
        )

        return event
