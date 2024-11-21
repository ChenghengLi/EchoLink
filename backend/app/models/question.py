"""Models"""
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.config import Base
import enum
from pydantic import BaseModel

# Enum for response status
class ResponseEnum(enum.Enum):
    waiting = "waiting"
    answered = "answered"
    rejected = "rejected"

# Questions table
class Question(Base):
    __tablename__ = "questions"

    question_id = Column(Integer, primary_key=True, index=True)
    listener_id = Column(Integer, ForeignKey('listeners.listener_id', ondelete="CASCADE"), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.artist_id', ondelete="CASCADE"), nullable=False)
    question_text = Column(Text, nullable=False)
    response_text = Column(Text, nullable=True)
    question_date = Column(DateTime, default=func.now(), nullable=False)
    response_date = Column(DateTime, nullable=True)
    response_status = Column(Enum(ResponseEnum), default=ResponseEnum.waiting)

    # Relationships to other tables
    listener = relationship("Listener")
    artist = relationship("Artist")

# Input data for question submission
class QuestionInput(BaseModel):
    listener_username: str
    artist_username: str
    question_text: str

# Input data for question response
class QuestionResponse(BaseModel):
    question_id: int
    response_text: str