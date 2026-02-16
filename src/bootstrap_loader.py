import json
import os
from datetime import datetime

from pymongo import MongoClient
from dotenv import load_dotenv

from hash_utils import generate_event_id

# --------------------------------------------------
# Configuração
# --------------------------------------------------

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]
events_collection = db["events_raw"]

BOOTSTRAP_PATH = "data/bootstrap"

EVENT_TYPE_MAP = {
    "orders_2023.json": "order_historical",
    "payments_2023.json": "payment_historical",
    "shipments_2023.json": "shipment_historical",
    "refunds_2023.json": "refund_historical",
}

# --------------------------------------------------
# Funções
# --------------------------------------------------

def load_json(file_path):
    with open(file_path, "r") as f:
        return json.load(f)


def process_file(filename):
    file_path = os.path.join(BOOTSTRAP_PATH, filename)
    records = load_json(file_path)

    event_type = EVENT_TYPE_MAP[filename]

    inserted = 0

    for record in records:
        event_time = record.get("created_at") or record.get("timestamp") or "1970-01-01T00:00:00"
        vendor = record.get("vendor", "unknown")

        event_id = generate_event_id(
            event_type=event_type,
            event_time=event_time,
            vendor=vendor,
            payload=record,
        )

        event_document = {
            "event_id": event_id,
            "event_type": event_type,
            "event_time": event_time,
            "vendor": vendor,
            "payload": record,
            "ingested_at": datetime.utcnow(),
            "source": "historical_bootstrap",
        }

        result = events_collection.update_one(
            {"event_id": event_id},
            {"$setOnInsert": event_document},
            upsert=True,
        )

        if result.upserted_id:
            inserted += 1

    print(f"{filename}: {inserted} novos eventos inseridos.")


# --------------------------------------------------
# Execução
# --------------------------------------------------

def main():
    for filename in EVENT_TYPE_MAP.keys():
        process_file(filename)

    print("✅ Bootstrap histórico concluído.")


if __name__ == "__main__":
    main()
