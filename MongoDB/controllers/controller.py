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

# Create Person, Loan, Credit History, Loan Financials
async def create_person_and_associated_data(person_data: Person, loan_data: Loan, credit_history_data: CreditHistory, loan_financials_data: LoanFinancials):
    # Insert person
    person_result = await person_collection.insert_one(person_data.dict())
    person_id = str(person_result.inserted_id)

    # Insert loan with person_id
    loan_data.person_id = person_id
    loan_result = await loan_collection.insert_one(loan_data.dict())
    loan_id = str(loan_result.inserted_id)

    # Insert credit history with person_id
    credit_history_data.person_id = person_id
    await credit_history_collection.insert_one(credit_history_data.dict())

    # Insert loan financials with loan_id
    loan_financials_data.loan_id = loan_id
    await loan_financials_collection.insert_one(loan_financials_data.dict())

    return {"message": "Person and associated data created successfully", "person_id": person_id, "loan_id": loan_id}

# Get all data related to a person
async def get_all_data_for_person(person_id: str):
    person = await person_collection.find_one({"_id": ObjectId(person_id)})
    loan = await loan_collection.find_one({"person_id": person_id})
    credit_history = await credit_history_collection.find_one({"person_id": person_id})
    loan_financials = await loan_financials_collection.find_one({"loan_id": loan["_id"]})
    
    return {
        "person": person,
        "loan": loan,
        "credit_history": credit_history,
        "loan_financials": loan_financials
    }

# Update Person and associated data
async def update_person_and_associated_data(person_id: str, person_data: Person, loan_data: Loan, credit_history_data: CreditHistory, loan_financials_data: LoanFinancials):
    # Update person
    await person_collection.update_one({"_id": ObjectId(person_id)}, {"$set": person_data.dict()})
    
    # Update loan
    await loan_collection.update_one({"person_id": person_id}, {"$set": loan_data.dict()})
    
    # Update credit history
    await credit_history_collection.update_one({"person_id": person_id}, {"$set": credit_history_data.dict()})
    
    # Update loan financials
    await loan_financials_collection.update_one({"loan_id": loan_data.person_id}, {"$set": loan_financials_data.dict()})
    
    return {"message": "Person and associated data updated successfully"}

# Delete Person and associated data
async def delete_person_and_associated_data(person_id: str):
    person = await person_collection.find_one({"_id": ObjectId(person_id)})
    if person:
        loan = await loan_collection.find_one({"person_id": person_id})
        credit_history = await credit_history_collection.find_one({"person_id": person_id})
        loan_financials = await loan_financials_collection.find_one({"loan_id": loan["_id"]})

        await person_collection.delete_one({"_id": ObjectId(person_id)})
        await loan_collection.delete_one({"_id": loan["_id"]})
        await credit_history_collection.delete_one({"_id": credit_history["_id"]})
        await loan_financials_collection.delete_one({"_id": loan_financials["_id"]})

        return {"message": "Person and associated data deleted successfully"}
    return {"message": "Person not found"}
