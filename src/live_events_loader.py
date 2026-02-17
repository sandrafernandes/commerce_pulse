#!/usr/bin/env python3
"""
Loads live JSONL events into MongoDB (append-only, raw ingestion)
"""

import json
from pathlib import Path
from pymongo.errors import BulkWriteError

#from config.mongo import get_mongo_client
#from src.config.mongo import get_mongo_client
from src.config.mongo_client import get_mongo_client


def load_events(jsonl_path: Path):
    client = get_mongo_client()
    db = client["commercepulse"]
    collection = db["events_raw"]

    docs = []

    with jsonl_path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(json.loads(line))

    if not docs:
        print(f"Nenhum evento encontrado em {jsonl_path}")
        return

    try:
        result = collection.insert_many(docs, ordered=False)
        print(f"{jsonl_path.name}: {len(result.inserted_ids)} eventos inseridos.")
    except BulkWriteError as e:
        print("Alguns eventos duplicados foram ignorados.")
        print(f"Inseridos: {e.details.get('nInserted', 0)}")


def main():
    base_dir = Path("data/live_events")

    if not base_dir.exists():
        print("Diretório data/live_events não encontrado.")
        return

    jsonl_files = list(base_dir.glob("*/events.jsonl"))

    if not jsonl_files:
        print("Nenhum ficheiro events.jsonl encontrado.")
        return

    for file in jsonl_files:
        load_events(file)


if __name__ == "__main__":
    main()
