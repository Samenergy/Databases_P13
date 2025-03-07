from fastapi import APIRouter
from controllers.controller import create_laptop, get_laptops, get_laptop_by_id, update_laptop, delete_laptop
from models.model import Laptop
from typing import List
from controllers.predict_controller import predict_price
from fastapi.responses import JSONResponse


router = APIRouter()

# Endpoint to create a new laptop
@router.post("/laptops/", response_model=Laptop)
async def add_laptop(laptop: Laptop):
    return await create_laptop(laptop)

# Endpoint to get all laptops
@router.get("/laptops/", response_model=List[Laptop])
async def get_all_laptops():
    # Await the asynchronous function
    laptops = await get_laptops()  # Await the coroutine
    return laptops

# Endpoint to get a single laptop by ID
@router.get("/laptops/{laptop_id}", response_model=Laptop)
async def get_laptop(laptop_id: str):
    return await get_laptop_by_id(laptop_id)

# Endpoint to update a laptop by ID
@router.put("/laptops/{laptop_id}", response_model=Laptop)
async def update_existing_laptop(laptop_id: str, laptop: Laptop):
    return await update_laptop(laptop_id, laptop)

# Endpoint to delete a laptop by ID
@router.delete("/laptops/{laptop_id}", response_model=Laptop)
async def delete_existing_laptop(laptop_id: str):
    return await delete_laptop(laptop_id)

@router.post("/predict")
def predict_laptop_price(laptop: Laptop):
    try:
        predicted_price = predict_price(laptop.dict())
        return JSONResponse(content={"Predicted_Price": round(predicted_price, 2)})
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
