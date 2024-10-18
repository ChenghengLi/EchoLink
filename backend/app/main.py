from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import core.models as models
from core.config import engine, SessionLocal
from crud.user import create_user

from contextlib import asynccontextmanager

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(bind=engine)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_user")
async def add_user(user: models.UserInput, db: Session = Depends(get_db)):
    #db_user = models.User(username=user.username)
    #db.add(db_user)
    #db.commit()
    #b.refresh(db_user)
    #return {"username": db_user.username, "id": db_user.id}  # Return a response
    pass

# Add a test user to the database on startup
@app.on_event("startup")
def init_db():
    db = SessionLocal()
    try:
        create_user(db, models.UserInput(username="test", email="test@test.com", password="test"))
    finally:
        db.close()