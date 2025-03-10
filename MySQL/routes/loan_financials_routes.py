from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import SessionLocal
from controllers.loan_financials_controller import get_all_loan_financials, create_loan_financials

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/loan_financials")
def read_loan_financials(db: Session = Depends(get_db)):
    return get_all_loan_financials(db)

@router.post("/loan_financials")
def add_loan_financials(financial_data: dict, db: Session = Depends(get_db)):
    return create_loan_financials(db, financial_data)
