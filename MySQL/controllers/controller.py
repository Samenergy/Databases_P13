from sqlalchemy.orm import Session
from models.person import Person
from models.loan import Loan
from models.loan_financials import LoanFinancials
from models.credit_history import CreditHistory
from pydantic import BaseModel
from typing import List, Optional


# Pydantic models for input format
class InputData(BaseModel):
    person_age: float
    person_gender: str
    person_education: str
    person_income: float
    person_emp_exp: int
    person_home_ownership: str
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: str
    loan_status: int


# Pydantic models for data validation
class PersonBase(BaseModel):
    age: float
    gender: str
    education: str
    income: float
    emp_exp: int
    home_ownership: str


class LoanBase(BaseModel):
    loan_amount: float
    loan_intent: str
    loan_status: int


class LoanFinancialsBase(BaseModel):
    interest_rate: float
    percent_income: float


class CreditHistoryBase(BaseModel):
    credit_score: int
    cred_hist_length: int
    previous_defaults: str


class PersonOut(PersonBase):
    id: int
    loans: Optional[List[LoanBase]] = []
    credit_history: Optional[List[CreditHistoryBase]] = []

    class Config:
        orm_mode = True


class LoanOut(LoanBase):
    id: int
    loan_financials: Optional[List[LoanFinancialsBase]] = []
    person_id: int

    class Config:
        orm_mode = True


class LoanFinancialsOut(LoanFinancialsBase):
    id: int
    loan_id: int

    class Config:
        orm_mode = True


class CreditHistoryOut(CreditHistoryBase):
    id: int
    person_id: int

    class Config:
        orm_mode = True


# CRUD functions for merging the models
def create_person_and_related_data(db: Session, input_data: InputData):
    # Step 1: Create the Person record
    db_person = Person(
        age=input_data.person_age,
        gender=input_data.person_gender,
        education=input_data.person_education,
        income=input_data.person_income,
        emp_exp=input_data.person_emp_exp,
        home_ownership=input_data.person_home_ownership
    )
    db.add(db_person)
    db.commit()
    db.refresh(db_person)

    # Step 2: Create the Loan record
    db_loan = Loan(
        person_id=db_person.id,
        loan_amount=input_data.loan_amnt,
        loan_intent=input_data.loan_intent,
        loan_status=input_data.loan_status
    )
    db.add(db_loan)
    db.commit()
    db.refresh(db_loan)

    # Step 3: Create the LoanFinancials record
    db_loan_financials = LoanFinancials(
        loan_id=db_loan.id,
        interest_rate=input_data.loan_int_rate,
        percent_income=input_data.loan_percent_income
    )
    db.add(db_loan_financials)
    db.commit()
    db.refresh(db_loan_financials)

    # Step 4: Create the CreditHistory record
    db_credit_history = CreditHistory(
        person_id=db_person.id,
        credit_score=input_data.credit_score,
        cred_hist_length=input_data.cb_person_cred_hist_length,
        previous_defaults=input_data.previous_loan_defaults_on_file
    )
    db.add(db_credit_history)
    db.commit()
    db.refresh(db_credit_history)

    return db_person, db_loan, db_loan_financials, db_credit_history


def get_all_persons(db: Session):
    return db.query(Person).all()


def get_person_by_id(db: Session, person_id: int):
    return db.query(Person).filter(Person.id == person_id).first()


def update_person(db: Session, person_id: int, person: PersonBase):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person:
        db_person.age = person.age
        db_person.gender = person.gender
        db_person.education = person.education
        db_person.income = person.income
        db_person.emp_exp = person.emp_exp
        db_person.home_ownership = person.home_ownership
        db.commit()
        db.refresh(db_person)
    return db_person


def delete_person(db: Session, person_id: int):
    db_person = db.query(Person).filter(Person.id == person_id).first()
    if db_person:
        db.delete(db_person)
        db.commit()
    return db_person
