""" Models """
from sqlalchemy import Column, Integer, String
from core.config import Base
from pydantic import BaseModel, field_validator
import re

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)

# Input user for login
class UserLogin(BaseModel):
    email: str
    password: str

    # Validator for password field
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long.')
        return v

    # Validator for email field
    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('Incorrect email format.')
        return v
    
# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Input user for register
class UserInput(UserLogin):
    username: str

    # Validator for username field
    @field_validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z_0-9]{4,16}$', v):
            raise ValueError('Username must be 4-16 characters long, containing only letters, numbers, and underscores.')
        return v