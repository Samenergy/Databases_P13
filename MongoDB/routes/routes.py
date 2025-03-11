from fastapi import APIRouter, HTTPException
from controllers.controller import create_all_models, get_person_by_id, update_person_data, update_loan_data, delete_person_data
from pydantic import BaseModel
from typing import Optional

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

# Create all models
@router.post("/create-all")
async def create_all(data: LoanRequest):
    return await create_all_models(data.dict())

# Read Operation
@router.get("/person/{person_id}")
async def read_person(person_id: str):
    person_data = await get_person_by_id(person_id)
    if not person_data:
        raise HTTPException(status_code=404, detail="Person not found")
    return person_data

# Update Person Operation
@router.put("/person/{person_id}")
async def update_person(person_id: str, data: LoanRequest):
    return await update_person_data(person_id, data.dict())

# Update Loan Operation
@router.put("/loan/{loan_id}")
async def update_loan(loan_id: str, data: LoanRequest):
    return await update_loan_data(loan_id, data.dict())

# Delete Person Operation
@router.delete("/person/{person_id}")
async def delete_person(person_id: str):
    return await delete_person_data(person_id)
