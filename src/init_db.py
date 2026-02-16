from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB]

collection = db["events_raw"]

# Garante unicidade do event_id (IDEMPOTÊNCIA)
collection.create_index("event_id", unique=True)

print("✅ Collection events_raw pronta com índice único em event_id")
