""" Models """
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from core.config import Base
from pydantic import BaseModel, ConfigDict
from typing import Optional

# Song table
class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    album = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    release_date = Column(String, nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), nullable=False)

    # Relationship with Artist
    artist = relationship("Artist", back_populates="songs")


# Pydantic model for song input
class SongInput(BaseModel):
    title: str
    release_date: str
    album: Optional[str] = None
    genre: Optional[str] = None
    artist_id: int

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)


# Pydantic model for song output
class SongOutput(BaseModel):
    title: str
    album: Optional[str] = None
    genre: Optional[str] = None
    release_date: str
    artist_name: str

    # Use ConfigDict for Pydantic v2
    model_config = ConfigDict(from_attributes=True)