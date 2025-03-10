from pydantic import BaseModel
from typing import Optional

# Pydantic model for creating/updating person data
class PersonCreate(BaseModel):
    age: float
    gender: str
    education: str
    income: float
    emp_exp: int
    home_ownership: str

class LoanCreate(BaseModel):
    loan_amount: float
    loan_intent: str
    loan_status: int

class LoanFinancialsCreate(BaseModel):
    interest_rate: float
    percent_income: float

class CreditHistoryCreate(BaseModel):
    credit_score: int
    cred_hist_length: float
    previous_defaults: str

class PersonResponse(PersonCreate, LoanCreate, LoanFinancialsCreate, CreditHistoryCreate):
    pass

# To ensure that we can merge the data as required by the user.
class PersonWithLoanResponse(BaseModel):
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

    class Config:
        orm_mode = True
