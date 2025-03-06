from fastapi import FastAPI
from routes.routes import router

app = FastAPI()

# Include the router
app.include_router(router)

# Main endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Laptop API!"}
