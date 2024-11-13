from fastapi import FastAPI

app = FastAPI()

from fastapi import HTTPException, Depends
import sqlalchemy as db
from dotenv import load_dotenv
import os
from core.database.connect import init_db
from app.api.user import router as user_router

# Load environment variables
load_dotenv()
init_db()


# Include the CRUD router
app.include_router(user_router, tags=["users"])

@app.get("/")
async def root():
    return {"message": "Hello World"}