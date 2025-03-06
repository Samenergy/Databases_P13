from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client.laptop_db
collection = db.laptops