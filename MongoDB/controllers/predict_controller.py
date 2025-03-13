import numpy as np
import tensorflow as tf
from config.db import collection
from models.predict import LoanApplication
from sklearn.preprocessing import LabelEncoder

# Load Keras model
model = tf.keras.models.load_model("/Users/samenergy/Documents/Projects/Databases_P13/Model/model.keras")

# Encode categorical values
gender_mapping = {"male": 0, "female": 1}
home_ownership_mapping = {"RENT": 0, "OWN": 1, "MORTGAGE": 2}
default_mapping = {"Yes": 1, "No": 0}

# Normalize the input data (same normalization as in training)
def normalize_data(data):
    return data / np.max(data, axis=0)

def preprocess_input(data: LoanApplication):
    """Converts user input into model-compatible format"""
    # Convert categorical variables using mappings
    encoded_data = np.array([
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
    ])
    
    # Normalize data like the training set
    encoded_data = normalize_data(encoded_data.reshape(1, -1))
    
    return encoded_data

def predict_loan(data: LoanApplication):
    """Predicts if a loan will be approved and saves the result in MongoDB"""
    input_data = preprocess_input(data)
    prediction = model.predict(input_data)
    
    # Threshold the prediction to determine loan approval
    loan_status = int(prediction[0][0] > 0.5)  # 1 if approved, 0 if rejected

    # Convert input data to dictionary for MongoDB
    data_dict = data.dict()
    data_dict["loan_status_prediction"] = "Approved" if loan_status == 1 else "Rejected"

    # Save to MongoDB
    collection.insert_one(data_dict)

    return data_dict
