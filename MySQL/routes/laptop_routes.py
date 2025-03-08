from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db
from controller import laptop_controller

router = APIRouter()

@router.get("/laptops", response_model=list)
def get_laptops(db: Session = Depends(get_db)):
    return laptop_controller.get_all_laptops(db)

@router.get("/laptops/{laptop_id}")
def get_laptop(laptop_id: int, db: Session = Depends(get_db)):
    laptop = laptop_controller.get_laptop_by_id(db, laptop_id)
    if not laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return laptop

@router.post("/laptops")
def add_laptop(laptop_data: dict, db: Session = Depends(get_db)):
    return laptop_controller.create_laptop(db, laptop_data)

@router.put("/laptops/{laptop_id}")
def update_laptop(laptop_id: int, laptop_data: dict, db: Session = Depends(get_db)):
    updated_laptop = laptop_controller.update_laptop(db, laptop_id, laptop_data)
    if not updated_laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return updated_laptop

@router.delete("/laptops/{laptop_id}")
def delete_laptop(laptop_id: int, db: Session = Depends(get_db)):
    deleted_laptop = laptop_controller.delete_laptop(db, laptop_id)
    if not deleted_laptop:
        raise HTTPException(status_code=404, detail="Laptop not found")
    return {"message": "Laptop deleted successfully"}
