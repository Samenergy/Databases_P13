from fastapi import APIRouter
from controllers.controller import create_all_models
from pydantic import BaseModel

router = APIRouter()

class LoanRequest(BaseModel):
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

@router.post("/create-all")
async def create_all(data: LoanRequest):
    return await create_all_models(data.dict())
