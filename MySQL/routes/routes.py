from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.controller import create_person_and_related_data, get_all_persons, get_person_by_id, update_person, delete_person
from controllers.controller import InputData, PersonBase
from config.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/person", response_model=PersonBase)
def add_person_with_loan(input_data: InputData, db: Session = Depends(get_db)):
    db_person, db_loan, db_loan_financials, db_credit_history = create_person_and_related_data(db, input_data)
    
    # You can combine the response in the desired format here
    return {
        "person_age": db_person.age,
        "person_gender": db_person.gender,
        "person_education": db_person.education,
        "person_income": db_person.income,
        "person_emp_exp": db_person.emp_exp,
        "person_home_ownership": db_person.home_ownership,
        "loan_amnt": db_loan.loan_amount,
        "loan_intent": db_loan.loan_intent,
        "loan_int_rate": db_loan_financials.interest_rate,
        "loan_percent_income": db_loan_financials.percent_income,
        "cb_person_cred_hist_length": db_credit_history.cred_hist_length,
        "credit_score": db_credit_history.credit_score,
        "previous_loan_defaults_on_file": db_credit_history.previous_defaults,
        "loan_status": db_loan.loan_status
    }


@router.get("/persons/", response_model=list[PersonBase])
def get_persons(db: Session = Depends(get_db)):
    return get_all_persons(db)


@router.get("/persons/{person_id}", response_model=PersonBase)
def get_person(person_id: int, db: Session = Depends(get_db)):
    db_person = get_person_by_id(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.put("/persons/{person_id}", response_model=PersonBase)
def update_person_data(person_id: int, person: PersonBase, db: Session = Depends(get_db)):
    db_person = update_person(db, person_id, person)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person


@router.delete("/persons/{person_id}", response_model=PersonBase)
def delete_person_data(person_id: int, db: Session = Depends(get_db)):
    db_person = delete_person(db, person_id)
    if db_person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return db_person
