from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from database.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)


