from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from controllers.credit_history_controller import get_all_credit_histories, create_credit_history

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/credit_histories")
def read_credit_histories(db: Session = Depends(get_db)):
    return get_all_credit_histories(db)

@router.post("/credit_histories")
def add_credit_history(credit_data: dict, db: Session = Depends(get_db)):
    return create_credit_history(db, credit_data)
