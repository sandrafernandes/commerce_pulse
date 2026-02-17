from src.config.mongo_client import get_mongo_client
import os

DB_NAME = os.getenv("MONGO_DB", "commercepulse")

def main():
    client = get_mongo_client()
    db = client[DB_NAME]
    events = db.events_raw

    report = {}

    report["total_events"] = events.count_documents({})

    report["missing_event_id"] = events.count_documents({
        "event_id": {"$exists": False}
    })

    report["future_events"] = events.count_documents({
        "$expr": {"$gt": ["$event_time", "$ingested_at"]}
    })

    report["by_type"] = list(events.aggregate([
        {"$group": {"_id": "$event_type", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]))

    print("\nEVENTS QUALITY REPORT")
    print("=====================")
    for k, v in report.items():
        print(f"{k}: {v}")

if __name__ == "__main__":
    main()
