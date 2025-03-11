from config.db import database
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


# Read Operation
async def get_person_by_id(person_id: str):
    person = await person_collection.find_one({"_id": ObjectId(person_id)})
    loan = await loan_collection.find_one({"person_id": person_id})
    credit_history = await credit_history_collection.find_one({"person_id": person_id})
    loan_financials = await loan_financials_collection.find_one({"loan_id": loan["loan_id"]})
    
    return {
        "person": person,
        "loan": loan,
        "credit_history": credit_history,
        "loan_financials": loan_financials
    }

# Update Operation
async def update_person_data(person_id: str, data: dict):
    updated_person = await person_collection.update_one(
        {"_id": ObjectId(person_id)},
        {"$set": data}
    )
    if updated_person.modified_count > 0:
        return {"message": "Person data updated successfully!"}
    return {"message": "No changes made!"}

async def update_loan_data(loan_id: str, data: dict):
    updated_loan = await loan_collection.update_one(
        {"_id": ObjectId(loan_id)},
        {"$set": data}
    )
    if updated_loan.modified_count > 0:
        return {"message": "Loan data updated successfully!"}
    return {"message": "No changes made!"}

# Delete Operation
async def delete_person_data(person_id: str):
    # Find the loan related to the person
    loan = await loan_collection.find_one({"person_id": person_id})
    
    if loan:
        loan_id = loan["_id"]  # Use the MongoDB _id as the loan_id
        
        # Delete the associated data from loan_financials collection using the loan_id
        await loan_financials_collection.delete_one({"loan_id": loan_id})

        # Delete the loan from the loan_collection
        await loan_collection.delete_one({"person_id": person_id})

    # Delete associated credit history
    await credit_history_collection.delete_many({"person_id": person_id})

    # Delete the person from the person_collection
    await person_collection.delete_one({"_id": ObjectId(person_id)})

    return {"message": "Person and related data deleted successfully!"}
