from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from controllers.controller import (
    create_person_with_loan_and_credit, get_all_persons_with_data,
    get_person_by_id
)
from models.schemas import PersonCreate, LoanCreate, LoanFinancialsCreate, CreditHistoryCreate
from config.database import get_db

router = APIRouter()

# Create a person with associated loan and credit history
@router.post("/persons/")
def create_person(
    person_data: PersonCreate,
    loan_data: LoanCreate,
    loan_financial_data: LoanFinancialsCreate,
    credit_history_data: CreditHistoryCreate,
    db: Session = Depends(get_db)
):
    return create_person_with_loan_and_credit(
        db, person_data, loan_data, loan_financial_data, credit_history_data
    )

# Get all persons with their data
@router.get("/persons/")
def get_all_persons(db: Session = Depends(get_db)):
    return get_all_persons_with_data(db)

# Get a person by ID with associated data
@router.get("/persons/{person_id}")
def get_person(person_id: int, db: Session = Depends(get_db)):
    return get_person_by_id(db, person_id)
