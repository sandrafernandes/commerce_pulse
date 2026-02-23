from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
mongo_db = os.getenv("MONGO_DB")

print("MONGO_URI:", mongo_uri)
print("MONGO_DB:", mongo_db)

client = MongoClient(mongo_uri)
db = client[mongo_db]

print("Bases de dados disponíveis:")
print(client.list_database_names())
