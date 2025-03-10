from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from controllers.loan_controller import get_all_loans, create_loan

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/loans")
def read_loans(db: Session = Depends(get_db)):
    return get_all_loans(db)

@router.post("/loans")
def add_loan(loan_data: dict, db: Session = Depends(get_db)):
    return create_loan(db, loan_data)
