from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.config import get_db
from models.user import UserLogin, Token

router = APIRouter()

@router.post("/")
def login_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    """
    User login, get an access token for future requests
    """
    pass
