from fastapi import FastAPI
from config.database import engine, Base
from routes import person_routes, loan_routes, credit_history_routes, loan_financials_routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Loan Management API")

# Include routes
app.include_router(person_routes.router, prefix="/api")
app.include_router(loan_routes.router, prefix="/api")
app.include_router(credit_history_routes.router, prefix="/api")
app.include_router(loan_financials_routes.router, prefix="/api")
