from sqlalchemy.orm import Session
from models.laptop import Laptop

def get_all_laptops(db: Session):
    return db.query(Laptop).all()

def get_laptop_by_id(db: Session, laptop_id: int):
    return db.query(Laptop).filter(Laptop.id == laptop_id).first()

def create_laptop(db: Session, laptop_data: dict):
    new_laptop = Laptop(**laptop_data)
    db.add(new_laptop)
    db.commit()
    db.refresh(new_laptop)
    return new_laptop

def update_laptop(db: Session, laptop_id: int, laptop_data: dict):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        return None
    for key, value in laptop_data.items():
        setattr(laptop, key, value)
    db.commit()
    return laptop

def delete_laptop(db: Session, laptop_id: int):
    laptop = db.query(Laptop).filter(Laptop.id == laptop_id).first()
    if not laptop:
        return None
    db.delete(laptop)
    db.commit()
    return laptop
