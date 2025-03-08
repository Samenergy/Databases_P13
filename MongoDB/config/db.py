from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# MongoDB URI and collection info from environment variables
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "LaptopPriceData")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "LaptopInfo")

# Create MongoClient and connect to the database
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
laptop_collection = db[COLLECTION_NAME]

def get_laptop_collection():
    return laptop_collection