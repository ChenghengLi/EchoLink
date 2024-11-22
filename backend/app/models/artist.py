""" Models """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config import Base
from typing import Optional
from pydantic import BaseModel

# Artist table
class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    genre = Column(String, nullable=True)
    bio = Column(String, nullable=True)

    # Relationship to the User table
    user = relationship("User")