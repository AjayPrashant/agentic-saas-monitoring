import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3:latest"  # or "mistral", "phi3" — your choice!

def generate_summary(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_URL, json=payload)
    if response.status_code != 200:
        print(f"[OllamaClient] Failed to generate: {response.status_code} {response.text}")
        return "LLM generation failed."

    result = response.json()
    return result.get("response", "").strip()
