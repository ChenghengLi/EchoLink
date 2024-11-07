from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.config import get_db
from crud.user import create_user as create_user_crud, \
    get_user_by_username as get_user_by_username_crud, \
    update_user as update_user_crud
import models.user as user_model

router = APIRouter()

@router.post("/user", response_model=user_model.UserOutput)
async def add_user(user_input: user_model.UserInput, db: Session = Depends(get_db)):
    user = create_user_crud(db, user_input)
    return user_model.UserOutput.model_validate(user)

@router.get("/username", response_model=user_model.UserOutput)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    user = get_user_by_username_crud(db, username)
    return user_model.UserOutput.model_validate(user)

@router.put("/username", response_model=user_model.UserOutput)
async def update_user(username: str, user_update: user_model.UserUpdate, db: Session = Depends(get_db)):
    user = update_user_crud(db, username, user_update)
    return user_model.UserOutput.model_validate(user)
