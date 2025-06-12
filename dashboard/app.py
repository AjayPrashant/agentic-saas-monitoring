import streamlit as st
import mlflow
import pandas as pd
from mlflow_tracking.mlflow_client import log_feedback
# Set MLFlow tracking URI (match your MLFlow container!)
mlflow.set_tracking_uri("http://localhost:5050")


# App title
st.title("📊 SaaS Monitoring Agent Dashboard")

# Sidebar - select experiment
experiments = mlflow.search_experiments()
experiment_names = [exp.name for exp in experiments]

selected_exp = st.sidebar.selectbox("Select Experiment", experiment_names)

# Load runs for selected experiment
experiment = [exp for exp in experiments if exp.name == selected_exp][0]
runs_df = mlflow.search_runs([experiment.experiment_id])

# Display latest anomalies
st.header("🚨 Latest Anomalies")

# Filter anomalies
anomalies_df = runs_df[runs_df["metrics.is_anomaly"] == 1.0]

# Show top 20 recent
if not anomalies_df.empty:
    display_df = anomalies_df[[
        "tags.mlflow.runName", 
        "metrics.anomaly_score", 
        "params.event_type", 
        "params.event_id", 
        "metrics.alert_triggered"
    ]].sort_values(by="metrics.anomaly_score", ascending=False).head(20)

    st.dataframe(display_df)
    # After showing anomalies:

if not anomalies_df.empty:
    selected_event_id = st.selectbox("Select event to give feedback", anomalies_df["params.event_id"].tolist())

    feedback = st.radio("Feedback:", ["Not Reviewed", "True Anomaly (+1)", "False Positive (-1)"])

    if st.button("Submit Feedback"):
        score = {"Not Reviewed": 0, "True Anomaly (+1)": 1, "False Positive (-1)": -1}[feedback]
        log_feedback(selected_event_id, score)
        st.success(f"Feedback submitted: {feedback} (score={score})")

else:
    st.info("No anomalies detected yet!")

# TODO: Add RAG notes + LLM summary once we log them to MLFlow!

st.markdown("---")
st.caption("Powered by LangGraph + Kafka + ChromaDB + Streamlit 🚀")
