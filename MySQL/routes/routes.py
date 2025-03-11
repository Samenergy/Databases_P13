from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from controllers.controller import create_person_with_details, get_person_with_details, delete_person
from models.schemas import PersonCreate

router = APIRouter()

@router.post("/create-person", response_model=dict)
def create_person_route(person_data: PersonCreate, db: Session = Depends(get_db)):
    return create_person_with_details(db, person_data)

@router.get("/person/{person_id}", response_model=dict)
def get_person_route(person_id: int, db: Session = Depends(get_db)):
    return get_person_with_details(db, person_id)

@router.delete("/person/{person_id}", response_model=dict)
def delete_person_route(person_id: int, db: Session = Depends(get_db)):
    return delete_person(db, person_id)
