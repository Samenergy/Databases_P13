from config.db import laptop_collection
from models.model import Laptop
from bson import ObjectId
from typing import List, Optional

# Convert MongoDB ObjectId to string for easy serialization
def laptop_helper(laptop):
    return {
        "_id": str(laptop["_id"]),  # Convert ObjectId to string
        "Brand": laptop["Brand"],  # Use matching field names (capitalized)
        "Processor": laptop["Processor"],
        "RAM_GB": laptop["RAM_GB"],
        "Storage": laptop["Storage"],
        "GPU": laptop["GPU"],
        "Screen_Size_inch": laptop["Screen_Size_inch"],
        "Resolution": laptop["Resolution"],
        "Battery_Life_Hours": laptop["Battery_Life_Hours"],
        "Weight_Kg": laptop["Weight_Kg"],
        "Operating_System": laptop["Operating_System"],
        "Price_Dollars": laptop["Price_Dollars"],
    }

# Create a new laptop
async def create_laptop(laptop_data: Laptop) -> dict:
    try:
        laptop = laptop_collection.insert_one(laptop_data.dict())
        new_laptop = laptop_collection.find_one({"_id": laptop.inserted_id})
        return {**laptop_helper(new_laptop), "message": "Laptop successfully created!"}
    except Exception as e:
        return {"message": f"Failed to create laptop: {str(e)}"}

# Read all laptops
async def get_laptops() -> dict:
    try:
        laptops = laptop_collection.find()
        laptop_list = [laptop_helper(laptop) for laptop in laptops]
        return {"laptops": laptop_list, "message": "All laptops fetched successfully."}
    except Exception as e:
        return {"message": f"Failed to fetch laptops: {str(e)}"}

# Read a single laptop by ID
async def get_laptop_by_id(laptop_id: str) -> dict:
    try:
        laptop = laptop_collection.find_one({"_id": ObjectId(laptop_id)})
        if laptop:
            return {**laptop_helper(laptop), "message": f"Laptop with ID {laptop_id} fetched successfully."}
        return {"message": f"Laptop with ID {laptop_id} not found."}
    except Exception as e:
        return {"message": f"Failed to fetch laptop by ID {laptop_id}: {str(e)}"}

# Update a laptop by ID
async def update_laptop(laptop_id: str, laptop_data: Laptop) -> dict:
    try:
        result = laptop_collection.update_one({"_id": ObjectId(laptop_id)}, {"$set": laptop_data.dict()})
        if result.modified_count > 0:
            updated_laptop = laptop_collection.find_one({"_id": ObjectId(laptop_id)})
            return {**laptop_helper(updated_laptop), "message": "Laptop updated successfully!"}
        return {"message": f"Laptop with ID {laptop_id} not found or no changes made."}
    except Exception as e:
        return {"message": f"Failed to update laptop by ID {laptop_id}: {str(e)}"}

# Delete a laptop by ID
async def delete_laptop(laptop_id: str) -> dict:
    try:
        laptop = laptop_collection.find_one({"_id": ObjectId(laptop_id)})
        if laptop:
            laptop_collection.delete_one({"_id": ObjectId(laptop_id)})
            return {**laptop_helper(laptop), "message": "Laptop deleted successfully."}
        return {"message": f"Laptop with ID {laptop_id} not found."}
    except Exception as e:
        return {"message": f"Failed to delete laptop by ID {laptop_id}: {str(e)}"}
