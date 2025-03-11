from fastapi import FastAPI
from routes.routes import router as crud_route

app = FastAPI()

# Include the CRUD routes for all models
app.include_router(crud_route.router, prefix="/data", tags=["Data Operations"])

@app.get("/")
async def root():
    return {"message": "Loan Management API is running!"}
