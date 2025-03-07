# app/controllers/laptop_controller.py
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from models.model import Laptop
from models.prediction import PredictionResponse

# Load models (use try-except to ensure loading is safe)
def load_models():
    try:
        rf_model = joblib.load('random_forest_model.pkl')
        encoder = joblib.load('onehot_encoder.pkl')
        scaler = joblib.load('scaler.pkl')
        return rf_model, encoder, scaler
    except FileNotFoundError:
        raise Exception("Models not found! Please save models first.")

rf_model, encoder, scaler = load_models()

# Prediction function
def predict_price(input_data: Laptop) -> PredictionResponse:
    input_df = pd.DataFrame([input_data.dict()])

    # List of expected features (based on your training model)
    expected_columns = ['Brand', 'Processor', 'RAM_GB', 'Storage', 'GPU', 'Screen_Size_inch', 'Resolution', 'Battery_Life_Hours', 'Weight_Kg', 'Operating_System']
    
    # Remove any unexpected columns
    input_df = input_df[expected_columns]

    # Preprocessing: Encoding categorical data
    encoded_input_data = encoder.transform(input_df[['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']])
    encoded_input_df = pd.DataFrame(encoded_input_data, columns=encoder.get_feature_names_out())

    # Scaling numerical features
    input_df[['RAM_GB', 'Screen_Size_inch', 'Battery_Life_Hours', 'Weight_Kg']] = scaler.transform(input_df[['RAM_GB', 'Screen_Size_inch', 'Battery_Life_Hours', 'Weight_Kg']])

    # Combine processed data
    final_input_df = pd.concat([input_df.drop(columns=['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']), encoded_input_df], axis=1)

    # Predict price
    predicted_price = rf_model.predict(final_input_df)
    return PredictionResponse(predicted_price=round(predicted_price[0], 2))
