import numpy as np
import tensorflow as tf
from config.db import collection
from models.predict import LoanApplication

# Load Keras model
model = tf.keras.models.load_model("model.keras")

# Encode categorical values
gender_mapping = {"male": 0, "female": 1}
home_ownership_mapping = {"RENT": 0, "OWN": 1, "MORTGAGE": 2}
default_mapping = {"Yes": 1, "No": 0}

def preprocess_input(data: LoanApplication):
    """Converts user input into model-compatible format"""
    return np.array([
        data.person_age,
        gender_mapping[data.person_gender],
        data.person_income,
        data.person_emp_exp,
        home_ownership_mapping[data.person_home_ownership],
        data.loan_amnt,
        data.loan_int_rate,
        data.loan_percent_income,
        data.cb_person_cred_hist_length,
        data.credit_score,
        default_mapping[data.previous_loan_defaults_on_file]
    ]).reshape(1, -1)  # Reshape for model input

def predict_loan(data: LoanApplication):
    """Predicts if a loan will be approved and saves the result in MongoDB"""
    input_data = preprocess_input(data)
    prediction = model.predict(input_data)
    loan_status = int(prediction[0][0] > 0.5)  # 1 if approved, 0 if rejected

    # Convert input data to dictionary for MongoDB
    data_dict = data.dict()
    data_dict["loan_status_prediction"] = "Approved" if loan_status == 1 else "Rejected"

    # Save to MongoDB
    collection.insert_one(data_dict)

    return data_dict
