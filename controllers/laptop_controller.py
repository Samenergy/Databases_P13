from bson import ObjectId
from config.db import collection
from models.laptop import Laptop
from fastapi import HTTPException

def laptop_serializer(laptop) -> dict:
    return {"id": str(laptop["_id"]), **laptop}

def create_laptop(laptop: Laptop):
    laptop_dict = laptop.dict()
    result = collection.insert_one(laptop_dict)
    return {"id": str(result.inserted_id), **laptop_dict}

def get_laptops():
    return [laptop_serializer(laptop) for laptop in collection.find()]

def get_laptop(laptop_id: str):
    laptop = collection.find_one({"_id": ObjectId(laptop_id)})
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop_serializer(laptop)

def update_laptop(laptop_id: str, laptop: Laptop):
    updated = collection.update_one({"_id": ObjectId(laptop_id)}, {"$set": laptop.dict()})
    if updated.matched_count == 0:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return {"message": "Laptop updated successfully"}

def delete_laptop(laptop_id: str):
    deleted = collection.delete_one({"_id": ObjectId(laptop_id)})
    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return {"message": "Laptop deleted successfully"}