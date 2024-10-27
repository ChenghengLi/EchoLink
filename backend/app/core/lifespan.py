from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy.orm import Session
from core.config import SessionLocal
from crud.user import create_user, get_user_by_username

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    #init_db()
    yield
    # Shutdown code (if needed)

# Add a test user to the database on startup
def init_db():
    db: Session = SessionLocal()
    try:
        user = get_user_by_username(db, "test")
        if not user:
            create_user(db, user.UserInput(username="test", email="test@test.com", password="test"))
    finally:
        db.close()
