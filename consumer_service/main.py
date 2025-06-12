import asyncio
import json
from aiokafka import AIOKafkaConsumer
from .langgraph_pipeline import run_agent_pipeline

async def consume():
    consumer = AIOKafkaConsumer(
        'saas_events',
        bootstrap_servers='localhost:9092',
        group_id='agent_consumer_group'
    )
    await consumer.start()
    try:
        async for msg in consumer:
            event = json.loads(msg.value.decode('utf-8'))
            print(f"Consumed event: {event}")
            await run_agent_pipeline(event)
    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())