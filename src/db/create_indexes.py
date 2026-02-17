from src.config.mongo_client import get_mongo_client
import os

DB_NAME = os.getenv("MONGO_DB", "commercepulse")

def main():
    client = get_mongo_client()
    db = client[DB_NAME]

    events = db.events_raw

    print("Criando índices...")

    events.create_index("event_id", unique=True)
    events.create_index("event_time")
    events.create_index("vendor")
    events.create_index("event_type")

    print("Índices criados com sucesso.")

if __name__ == "__main__":
    main()
