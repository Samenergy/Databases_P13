from fastapi import FastAPI
from routes import laptop_routes
from models.database import init_db

app = FastAPI()

# Initialize database
init_db()

# Include routes
app.include_router(laptop_routes.router, prefix="/api")

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Laptop API"}
