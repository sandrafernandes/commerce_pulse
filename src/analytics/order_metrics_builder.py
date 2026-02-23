from src.config.mongo_client import get_mongo_client
from datetime import datetime
import os

DB_NAME = os.getenv("MONGO_DB", "commercepulse")


def parse_iso(ts):
    """
    Aceita:
    - ISO string (com ou sem Z)
    - timestamp int / float
    """
    if ts is None:
        return None

    # Caso seja timestamp (vendor_c)
    if isinstance(ts, (int, float)):
        return datetime.utcfromtimestamp(ts)

    # Caso seja string
    if isinstance(ts, str):
        return datetime.fromisoformat(ts.replace("Z", ""))

    return None


def main():
    client = get_mongo_client()
    db = client[DB_NAME]

    events = db.events_curated
    metrics = db.order_metrics

    orders = {}

    for ev in events.find():
        order_id = ev.get("order_id")
        if not order_id:
            continue

        t = parse_iso(ev.get("event_time"))
        if not t:
            continue

        rec = orders.setdefault(order_id, {
            "order_id": order_id,
            "created_at": None,
            "paid_at": None,
            "delivered_at": None,
            "refund_count": 0
        })

        et = ev["event_type"]

        if et == "order_created":
            rec["created_at"] = t
        elif et == "payment_succeeded":
            rec["paid_at"] = t
        elif et == "shipment_updated":
            rec["delivered_at"] = t
        elif et == "refund_issued":
            rec["refund_count"] += 1

    for doc in orders.values():
        metrics.update_one(
            {"order_id": doc["order_id"]},
            {"$set": doc},
            upsert=True
        )

    print(f"Métricas geradas para {len(orders)} encomendas.")


if __name__ == "__main__":
    main()
