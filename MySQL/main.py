from routes import routes
from fastapi import FastAPI
from config.database import engine, Base
from routes.routes import routes

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Loan Management API")

# Include routes
app.include_router(routes.router, prefix="/api")
