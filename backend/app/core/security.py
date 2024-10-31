""" Security related methods """
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from jose import jwt
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
