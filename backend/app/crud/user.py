""" User related CRUD methods """
from sqlalchemy.orm import Session
from models.user import User, UserInput
from core.security import get_password_hash

# User creation
def create_user(db: Session, user_input: UserInput) -> User:
    user = User(username=user_input.username, email=user_input.email,
                hashed_password = get_password_hash(user_input.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Get user by username
def get_user_by_username(db: Session, username: str) -> User:
    return db.query(User).filter(User.username == username).first()

# Get user by email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()

# Get user by id
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()
