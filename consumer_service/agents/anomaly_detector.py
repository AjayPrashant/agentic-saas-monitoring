class AnomalyDetectorAgent:
    async def __call__(self, event):
        from random import random
        event["anomaly_score"] = random()
        event["is_anomaly"] = event["anomaly_score"] > 0.8
        print(f"[AnomalyDetectorAgent] anomaly_score: {event['anomaly_score']}, is_anomaly: {event['is_anomaly']}")
        return event