# app/controllers/laptop_controller.py
import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from models.model import Laptop
from models.prediction import PredictionResponse
import os
import joblib

def load_models(models_dir="saved_models"):
    """
    Load machine learning models from the specified directory
    
    Args:
        models_dir (str): Path to the directory containing saved models
        
    Returns:
        tuple: (rf_model, encoder, scaler)
    """
    try:
        # Create full paths to model files
        rf_model_path = os.path.join(models_dir, 'random_forest_model.pkl')
        encoder_path = os.path.join(models_dir, 'onehot_encoder.pkl')
        scaler_path = os.path.join(models_dir, 'scaler.pkl')
        
        # Load models from the specified directory
        rf_model = joblib.load(rf_model_path)
        encoder = joblib.load(encoder_path)
        scaler = joblib.load(scaler_path)
        
        return rf_model, encoder, scaler
    except FileNotFoundError as e:
        raise Exception(f"Models not found in directory '{models_dir}'! Please save models first. Error: {str(e)}")

# You can specify a different directory when calling the function
rf_model, encoder, scaler = load_models("/Users/samenergy/Documents/Projects/Databases_P13/MongoDB/saved_models")

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
