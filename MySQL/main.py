from routes.routes import router
from fastapi import FastAPI
from config.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Loan Management API")

# Include routes
app.include_router(router, prefix="/api")
