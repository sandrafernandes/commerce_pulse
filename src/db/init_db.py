from src.config.mongo_client import get_database

def init_database():
    db = get_database()

    collections = [
        "customers",
        "orders",
        "products",
        "events"
    ]

    existing_collections = db.list_collection_names()

    for collection in collections:
        if collection not in existing_collections:
            db.create_collection(collection)
            print(f"Coleção criada: {collection}")
        else:
            print(f"Coleção já existe: {collection}")

if __name__ == "__main__":
    init_database()
