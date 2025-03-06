from fastapi import FastAPI
from routes.laptop_routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
def root():
    return {"message": "Welcome to the Laptop Price API"}