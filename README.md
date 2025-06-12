# SaaS Monitoring AI Agentic System 🚨🤖

A production-grade AI Agent system for real-time SaaS event monitoring — using LangGraph, Kafka, RAG (ChromaDB), MLFlow, and Slack alerts.

## 🔧 Features

- 🧠 Modular LangGraph agent pipeline: Event Classifier → Anomaly Detector → RAG → (LLM) → Slack Alerts
- ⚙️ Real-time event stream ingestion via Apache Kafka
- 🗃️ ChromaDB vector retrieval (RAG) with metadata filtering
- 📊 MLFlow tracking and feedback loop
- 📺 Streamlit dashboard for live anomaly monitoring
- 🔁 Engineer-in-the-loop feedback agent
- 📦 Dockerized and scalable architecture

## 📦 Tech Stack

- **LangGraph**, **Kafka**, **MLFlow**, **ChromaDB**, **Sentence Transformers**
- **Streamlit**, **Slack Webhooks**
- **Docker Compose**, **Python 3.11**

## 🚀 Getting Started

```bash
git clone https://github.com/<your-username>/ai-agentic-saas-monitoring.git
cd ai-agentic-saas-monitoring
docker-compose up -d
