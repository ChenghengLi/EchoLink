""" Models """
from sqlalchemy import Column, Integer, String
from core.config import Base
from pydantic import BaseModel

# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)

# Input user
class UserInput(BaseModel):
    username: str
    email: str
    password: str
