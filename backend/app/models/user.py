""" Models """
from sqlalchemy import Column, Integer, String
from core.config import Base
from pydantic import BaseModel

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, index=True, primary_key=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, index=True, unique=True)
    hashed_password = Column(String)

# Input user
class UserInput(BaseModel):
    username: str
    email: str
    password: str
