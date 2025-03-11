from fastapi import APIRouter
from controllers.controller import create_person_and_associated_data, get_all_data_for_person, update_person_and_associated_data, delete_person_and_associated_data
from models.person import Person
from models.loan import Loan
from models.credit_history import CreditHistory
from models.loan_financials import LoanFinancials

router = APIRouter()

# CRUD operations for all models
@router.post("/create")
async def create_data(person: Person, loan: Loan, credit_history: CreditHistory, loan_financials: LoanFinancials):
    return await crud_controller.create_person_and_associated_data(person, loan, credit_history, loan_financials)

@router.get("/get/{person_id}")
async def get_data(person_id: str):
    return await crud_controller.get_all_data_for_person(person_id)

@router.put("/update/{person_id}")
async def update_data(person_id: str, person: Person, loan: Loan, credit_history: CreditHistory, loan_financials: LoanFinancials):
    return await crud_controller.update_person_and_associated_data(person_id, person, loan, credit_history, loan_financials)

@router.delete("/delete/{person_id}")
async def delete_data(person_id: str):
    return await crud_controller.delete_person_and_associated_data(person_id)
