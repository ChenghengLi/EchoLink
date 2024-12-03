""" Models """
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config import Base

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

    # Relationship with Songs
    songs = relationship("Song", back_populates="artist", cascade="all, delete-orphan")


# Pydantic model for the response
class ArtistOutput(BaseModel):
    username: str
    genre: str

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)