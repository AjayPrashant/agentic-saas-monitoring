import json
import random
import asyncio
from datetime import datetime
from aiokafka import AIOKafkaProducer

EVENT_TYPES = [
    "user_login",
    "feature_usage",
    "subscription_cancellation",
    "error",
    "support_ticket_created"
]

# Generate a random event
def generate_event():
    event_type = random.choice(EVENT_TYPES)
    event = {
        "event_id": f"evt_{random.randint(1000, 9999)}",
        "event_type": event_type,
        "user_id": f"user_{random.randint(1, 100)}",
        "timestamp": datetime.utcnow().isoformat(),
        "metadata": {
            "feature_name": random.choice(["dashboard", "analytics", "reporting"]) if event_type == "feature_usage" else "",
            "error_code": random.choice(["500_INTERNAL", "404_NOT_FOUND"]) if event_type == "error" else "",
            "device": random.choice(["macos_chrome", "windows_firefox", "linux_edge"]),
            "ip_address": f"192.168.1.{random.randint(1, 255)}"
        }
    }
    return event

# Main async producer loop
async def produce():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

    # Start the producer
    await producer.start()
    try:
        while True:
            event = generate_event()
            await producer.send_and_wait('saas_events', event)
            print(f"Produced event: {event}")
            await asyncio.sleep(random.uniform(0.5, 2))
    finally:
        await producer.stop()

# Entry point
if __name__ == "__main__":
    asyncio.run(produce())
