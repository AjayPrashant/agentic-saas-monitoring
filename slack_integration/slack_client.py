import yaml
import requests
import os

# Load config
with open(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'), 'r') as f:
    config = yaml.safe_load(f)

WEBHOOK_URL = config['slack']['webhook_url']

def send_alert(alert_msg):
    payload = {
        "text": alert_msg
    }

    response = requests.post(WEBHOOK_URL, json=payload)

    if response.status_code != 200:
        print(f"[SlackClient] Failed to send alert: {response.status_code} {response.text}")
    else:
        print(f"[SlackClient] ✅ Alert sent to Slack!")

    