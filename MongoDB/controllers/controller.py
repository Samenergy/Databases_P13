from config.db import database
from models.person import Person
from models.loan import Loan
from models.credit_history import CreditHistory
from models.loan_financials import LoanFinancials
from bson import ObjectId

person_collection = database["persons"]
loan_collection = database["loans"]
credit_history_collection = database["credit_history"]
loan_financials_collection = database["loan_financials"]

async def create_all_models(data: dict):
    # Create Person
    person_data = {
        "person_age": data["person_age"],
        "person_gender": data["person_gender"],
        "person_education": data["person_education"],
        "person_income": data["person_income"],
        "person_emp_exp": data["person_emp_exp"],
        "person_home_ownership": data["person_home_ownership"]
    }
    person_result = await person_collection.insert_one(person_data)
    person_id = str(person_result.inserted_id)

    # Create Loan
    loan_data = {
        "person_id": person_id,
        "loan_amnt": data["loan_amnt"],
        "loan_intent": data["loan_intent"],
        "loan_status": data["loan_status"]
    }
    loan_result = await loan_collection.insert_one(loan_data)
    loan_id = str(loan_result.inserted_id)

    # Create Credit History
    credit_history_data = {
        "person_id": person_id,
        "credit_score": data["credit_score"],
        "cb_person_cred_hist_length": data["cb_person_cred_hist_length"],
        "previous_loan_defaults_on_file": data["previous_loan_defaults_on_file"]
    }
    await credit_history_collection.insert_one(credit_history_data)

    # Create Loan Financials
    loan_financials_data = {
        "loan_id": loan_id,
        "loan_int_rate": data["loan_int_rate"],
        "loan_percent_income": data["loan_percent_income"]
    }
    await loan_financials_collection.insert_one(loan_financials_data)

    return {"message": "Data saved successfully!", "person_id": person_id, "loan_id": loan_id}
