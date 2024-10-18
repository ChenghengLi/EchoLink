from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database.models as models
from database.config import engine, SessionLocal
from contextlib import asynccontextmanager

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    add_test_user()
    yield
    # Shutdown code (if needed)

app = FastAPI(lifespan=lifespan)
models.Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Define the Pydantic model for user input
class User(BaseModel):
    username: str

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/add_user")
async def add_user(user: User, db: Session = Depends(get_db)):
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"username": db_user.username, "id": db_user.id}  # Return a response

def add_test_user():
    db = SessionLocal()
    try:
        test_user = models.User(username="test")
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"Test user added with ID: {test_user.id}")
    finally:
        db.close()