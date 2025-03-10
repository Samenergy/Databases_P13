from fastapi import FastAPI
from routes.routes import router

app = FastAPI()

# Include the routes
app.include_router(router)
