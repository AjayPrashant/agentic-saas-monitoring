import mlflow

# Set tracking URI to local MLFlow server
mlflow.set_tracking_uri("http://localhost:5050")

# Set experiment name
mlflow.set_experiment("Agentic SaaS Monitoring")

def log_event_metrics(event_id, event_type, anomaly_score, is_anomaly, alert_triggered):
    with mlflow.start_run(run_name=f"event_{event_id}"):
        mlflow.log_param("event_id", event_id)
        mlflow.log_param("event_type", event_type)
        mlflow.log_metric("anomaly_score", anomaly_score)
        mlflow.log_metric("is_anomaly", float(is_anomaly))
        mlflow.log_metric("alert_triggered", float(alert_triggered))
        print(f"[MLFlowClient] ✅ Event {event_id} logged to MLFlow.")

def log_feedback(event_id, feedback_score):
    with mlflow.start_run(run_name=f"feedback_{event_id}", nested=True):
        mlflow.log_param("event_id", event_id)
        mlflow.log_metric("feedback_score", feedback_score)
