from pydantic import BaseModel
from typing import Literal

class LoanApplication(BaseModel):
    person_age: float
    person_gender: Literal["male", "female"]
    person_education: str
    person_income: float
    person_emp_exp: float
    person_home_ownership: Literal["RENT", "OWN", "MORTGAGE"]
    loan_amnt: float
    loan_intent: str
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: float
    credit_score: int
    previous_loan_defaults_on_file: Literal["Yes", "No"]
