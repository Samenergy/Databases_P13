from sqlalchemy.orm import Session
from models.person import Person
from models.loan import Loan
from models.loan_financials import LoanFinancials
from models.credit_history import CreditHistory
from pydantic import BaseModel
from typing import List, Optional


# Pydantic models for input data
class CreatePersonLoanCreditHistory(BaseModel):
    person_age: float
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_status: int
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: str


class PersonOut(BaseModel):
    id: int
    age: float
    gender: str
    education: str
    income: float
    emp_exp: int
    home_ownership: str
    loans: Optional[List[Loan]] = []
    credit_history: Optional[List[CreditHistory]] = []

    class Config:
        orm_mode = True


class LoanOut(BaseModel):
    id: int
    loan_amount: float
    loan_intent: str
    loan_status: int
    interest_rate: float
    percent_income: float

    class Config:
        orm_mode = True


class CreditHistoryOut(BaseModel):
    id: int
    credit_score: int
    cred_hist_length: float
    previous_defaults: str

    class Config:
        orm_mode = True


def create_person_with_loan_and_credit_history(db: Session, data: CreatePersonLoanCreditHistory):
    # Create Person record
    db_person = Person(
        age=data.person_age,
        gender=data.person_gender,
        education=data.person_education,
        income=data.person_income,
        emp_exp=data.person_emp_exp,
        home_ownership=data.person_home_ownership
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

    # Create Loan record
    db_loan = Loan(
        person_id=db_person.id,
        loan_amount=data.loan_amnt,
        loan_intent=data.loan_intent,
        loan_status=data.loan_status
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    # Create LoanFinancials record
    db_loan_financials = LoanFinancials(
        loan_id=db_loan.id,
        interest_rate=data.loan_int_rate,
        percent_income=data.loan_percent_income
    )
    db.add(db_loan_financials)
    db.commit()
    db.refresh(db_loan_financials)

    # Create CreditHistory record
    db_credit_history = CreditHistory(
        person_id=db_person.id,
        credit_score=data.credit_score,
        cred_hist_length=data.cb_person_cred_hist_length,
        previous_defaults=data.previous_loan_defaults_on_file
    )
    db.add(db_credit_history)
    db.commit()
    db.refresh(db_credit_history)

    return db_person


def get_all_persons(db: Session):
    return db.query(Person).all()


def get_person_by_id(db: Session, person_id: int):
    return db.query(Person).filter(Person.id == person_id).first()


def update_person(db: Session, person_id: int, person: CreatePersonLoanCreditHistory):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person:
        db_person.age = person.person_age
        db_person.gender = person.person_gender
        db_person.education = person.person_education
        db_person.income = person.person_income
        db_person.emp_exp = person.person_emp_exp
        db_person.home_ownership = person.person_home_ownership
        db.commit()
        db.refresh(db_person)
    return db_person


def delete_person(db: Session, person_id: int):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person
