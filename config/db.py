from pymongo import MongoClient
import os

# MongoDB URI
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create MongoClient and connect to the database
client = MongoClient(MONGO_URI)
db = client['LaptopPriceData']  # Database Name
laptop_collection = db['LaptopInfo']  # Collection Name
