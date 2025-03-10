from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers import (
    create_person_with_loan_and_credit_history,
    get_all_persons,
    get_person_by_id,
    update_person,
    delete_person
)
from models import CreatePersonLoanCreditHistory, PersonOut
from config.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/persons/", response_model=PersonOut)
def add_person(data: CreatePersonLoanCreditHistory, db: Session = Depends(get_db)):
    return create_person_with_loan_and_credit_history(db, data)


@router.get("/persons/", response_model=List[PersonOut])
def get_persons(db: Session = Depends(get_db)):
    return get_all_persons(db)


@router.get("/persons/{person_id}", response_model=PersonOut)
def get_person(person_id: int, db: Session = Depends(get_db)):
    db_person = get_person_by_id(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.put("/persons/{person_id}", response_model=PersonOut)
def update_person_data(person_id: int, data: CreatePersonLoanCreditHistory, db: Session = Depends(get_db)):
    db_person = update_person(db, person_id, data)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.delete("/persons/{person_id}", response_model=PersonOut)
def delete_person_data(person_id: int, db: Session = Depends(get_db)):
    db_person = delete_person(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
