from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from controllers.person_controller import get_all_persons, create_person

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/persons")
def read_persons(db: Session = Depends(get_db)):
    return get_all_persons(db)

@router.post("/persons")
def add_person(person_data: dict, db: Session = Depends(get_db)):
    return create_person(db, person_data)
