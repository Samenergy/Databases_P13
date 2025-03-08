# app/models/prediction.py
from pydantic import BaseModel

class PredictionResponse(BaseModel):
    predicted_price: float
