from fastapi import APIRouter, Depends, HTTPException
from pytest import Session
from core.config import get_db
from core.security import CurrentUser
from models.user import UserLogin, Token
from crud.user import authenticate

router = APIRouter()

@router.post("/")
def login_access_token(user_login: UserLogin, db: Session = Depends(get_db)) -> Token:
    """
    User login, get an access token for future requests
    """
    try:
        return Token(access_token=authenticate(db, user_login))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/check_token/")
def login_check_token(user: CurrentUser):
    """
    Check access token is valid
    """
    pass
