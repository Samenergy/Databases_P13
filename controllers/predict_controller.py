import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from config.db import get_collection

# Global variables
encoder = None
scaler = None
rf_model = None

def load_data_from_mongo():
    # Fetch the data from MongoDB collection
    data = pd.DataFrame(list(get_collection().find()))
    data.drop(columns=['_id'], inplace=True)  # Drop MongoDB `_id` column
    return data

def preprocess_data(data: pd.DataFrame):
    global encoder, scaler
    # One-Hot Encode categorical columns
    categorical_columns = ['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']
    encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
    encoded_categorical_data = encoder.fit_transform(data[categorical_columns])
    encoded_df = pd.DataFrame(encoded_categorical_data, columns=encoder.get_feature_names_out(categorical_columns))
    
    # Merge the encoded categorical columns with the rest of the data
    data_encoded = pd.concat([data.drop(columns=categorical_columns), encoded_df], axis=1)
    
    # Feature scaling for numerical columns
    scaler = StandardScaler()
    numerical_columns = ['RAM_GB', 'Screen_Size_inch', 'Battery_Life_Hours', 'Weight_Kg']
    data_encoded[numerical_columns] = scaler.fit_transform(data_encoded[numerical_columns])
    
    return data_encoded

def train_model(data_encoded: pd.DataFrame):
    global rf_model
    # Define features and target variable
    X = data_encoded.drop(columns=['Price_Dollars'])
    y = data_encoded['Price_Dollars']
    
    # Train the Random Forest Regressor
    rf_model = RandomForestRegressor(random_state=42)
    rf_model.fit(X, y)
    
    return rf_model

def predict_price(input_data):
    global encoder, scaler, rf_model
    
    if encoder is None or scaler is None or rf_model is None:
        raise Exception("The model is not trained or the preprocessing pipeline is not initialized.")
    
    # Convert input data into DataFrame
    input_df = pd.DataFrame([input_data])
    
    # One-hot encode categorical columns
    encoded_input_data = encoder.transform(input_df[['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']])
    encoded_input_df = pd.DataFrame(encoded_input_data, columns=encoder.get_feature_names_out(['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']))
    
    # Scale numerical columns
    input_df[['RAM_GB', 'Screen_Size_inch', 'Battery_Life_Hours', 'Weight_Kg']] = scaler.transform(input_df[['RAM_GB', 'Screen_Size_inch', 'Battery_Life_Hours', 'Weight_Kg']])
    
    # Combine the encoded categorical and scaled numerical data
    final_input_df = pd.concat([input_df.drop(columns=['Brand', 'Processor', 'Storage', 'GPU', 'Resolution', 'Operating_System']),
                                encoded_input_df], axis=1)
    
    # Predict the price using the trained Random Forest model
    predicted_price = rf_model.predict(final_input_df)
    
    return predicted_price[0]

# Main execution flow
if __name__ == "__main__":
    try:
        # Load data from MongoDB
        data = load_data_from_mongo()
        
        # Preprocess data
        data_encoded = preprocess_data(data)
        
        # Train model
        rf_model = train_model(data_encoded)
        
        # Example input data for prediction
        new_laptop = {
            'Brand': 'HP',
            'Processor': 'AMD Ryzen 5',
            'RAM_GB': 4,
            'Storage': '1TB SSD',
            'GPU': 'AMD Radeon RX 6800',
            'Screen_Size_inch': 14.0,
            'Resolution': '3840x2160',
            'Battery_Life_Hours': 7.5,
            'Weight_Kg': 2.19,
            'Operating_System': 'FreeDOS'
        }
        
        # Predict price
        predicted_price = predict_price(new_laptop)
        print(f"Predicted Price for the new laptop: ${predicted_price:.2f}")
    
    except Exception as e:
        print(f"Error: {e}")

