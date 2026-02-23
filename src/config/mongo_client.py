import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongo_client():
    mongo_uri = os.getenv("MONGO_URI")
    if not mongo_uri:
        raise ValueError("MONGO_URI não encontrada no .env")

    return MongoClient(mongo_uri)

def get_database():
    client = get_mongo_client()
    db_name = os.getenv("MONGO_DB")
    if not db_name:
        raise ValueError("MONGO_DB não encontrada no .env")

    return client[db_name]
