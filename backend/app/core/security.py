""" Security related methods """
from datetime import datetime, timedelta
from typing import Annotated
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import ValidationError
from pytest import Session
from core.config import get_db
from fastapi import Depends, HTTPException, status
from models.user import User, TokenPayload
from dotenv import load_dotenv
import os
from jose import jwt, JWTError, ExpiredSignatureError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Load environment variables from .env file
load_dotenv()

# Data from .env file
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
EXPIRE_DELTA = timedelta(days=int(os.getenv("ACCESS_TOKEN_EXPIRE_DAYS")))

# Function to create JWT token
def create_access_token(subject) -> str:
    expire = datetime.utcnow() + EXPIRE_DELTA
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Security scheme for token authentication
security = HTTPBearer()

# Dependency to get user and verify token
def get_current_user(db: Session = Depends(get_db), 
                     credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token expired") 
    except (JWTError, ValidationError):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")
    user = db.get(User, token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    # JWT valid for the user, check if it is the one in the database
    if user.token != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return user

# User annotation
CurrentUser = Annotated[User, Depends(get_current_user)]
