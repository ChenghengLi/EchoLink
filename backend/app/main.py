from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import database.models as models
from database.config import engine, SessionLocal

app = FastAPI()
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



# Add a test user to the database on startup
@app.on_event("startup")
def init_db():
    #add_test_user()
    pass


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
