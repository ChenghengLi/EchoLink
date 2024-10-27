from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import get_db
from crud.user import create_user as create_user_crud, \
    get_user_by_id as get_user_by_id_crud, \
    get_user_by_username as get_user_by_username_crud, \
    get_user_by_email as get_user_by_email_crud
import models.user as user

router = APIRouter()

@router.post("/user")
async def add_user(user_input: user.UserInput, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user_by_email = get_user_by_email_crud(db, user_input.email)
    if existing_user_by_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check if username is already registered
    existing_user_by_username = get_user_by_username_crud(db, user_input.username)
    if existing_user_by_username:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Proceed with user creation if no duplicates are found
    user = create_user_crud(db, user_input)

    # Return the created user
    return user

@router.get("/get_user/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id_crud(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/get_user_by_username/{username}")
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    db_user = get_user_by_username_crud(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/get_user_by_email/{email}")
async def get_user_by_email(email: str, db: Session = Depends(get_db)):
    db_user = get_user_by_email_crud(db, email)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
