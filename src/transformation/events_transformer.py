import os
import json
from src.config.mongo_client import get_mongo_client

DB_NAME = os.getenv("MONGO_DB", "commercepulse")


def normalize_payload(raw_payload):
    """
    Converte qualquer payload em dict seguro
    """
    if isinstance(raw_payload, dict):
        return raw_payload

    if isinstance(raw_payload, str):
        try:
            parsed = json.loads(raw_payload)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass

    return {}


def extract_order_id(raw_payload):
    data = normalize_payload(raw_payload)

    if not data:
        return None

    if "orderRef" in data:
        return data["orderRef"]

    if "order_id" in data:
        return data["order_id"]

    if isinstance(data.get("order"), dict):
        return data["order"].get("id")

    if isinstance(data.get("order"), str):
        return data["order"]

    return None


def main():
    client = get_mongo_client()
    db = client[DB_NAME]

    raw_col = db.events_raw
    curated_col = db.events_curated

    transformed = 0

    for ev in raw_col.find():
        order_id = extract_order_id(ev.get("payload"))

        doc = {
            "event_id": ev.get("event_id"),
            "event_type": ev.get("event_type"),
            "vendor": ev.get("vendor"),
            "event_time": ev.get("event_time"),
            "order_id": order_id,
            "ingested_at": ev.get("ingested_at"),
        }

        result = curated_col.update_one(
            {"event_id": doc["event_id"]},
            {"$setOnInsert": doc},
            upsert=True,
        )

        if result.upserted_id:
            transformed += 1

    print(f"Transformados {transformed} eventos.")


if __name__ == "__main__":
    main()
