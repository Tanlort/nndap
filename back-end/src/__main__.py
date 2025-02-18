from fastapi import FastAPI
from .database import engine, Base
from .routes import router
# Create the FastAPI application
app = FastAPI()

# Include the routes
app.include_router(router)