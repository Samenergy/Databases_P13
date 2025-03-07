# app/main.py
from fastapi import FastAPI
from routes.routes import router as laptop_router

app = FastAPI()

# Include the laptop-related routes
app.include_router(laptop_router, prefix="/laptop", tags=["laptop"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Laptop Price Prediction API"}
