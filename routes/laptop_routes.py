from fastapi import APIRouter
from models.laptop import Laptop
from controllers.laptop_controller import create_laptop, get_laptops, get_laptop, update_laptop, delete_laptop

router = APIRouter()

@router.post("/laptops/")
def create(laptop: Laptop):
    return create_laptop(laptop)

@router.get("/laptops/")
def read_all():
    return get_laptops()

@router.get("/laptops/{laptop_id}")
def read_one(laptop_id: str):
    return get_laptop(laptop_id)

@router.put("/laptops/{laptop_id}")
def update(laptop_id: str, laptop: Laptop):
    return update_laptop(laptop_id, laptop)

@router.delete("/laptops/{laptop_id}")
def delete(laptop_id: str):
    return delete_laptop(laptop_id)
