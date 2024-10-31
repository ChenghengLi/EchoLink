""" User related CRUD methods """
from sqlalchemy.orm import Session
from models.user import User, UserInput, UserLogin
from core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException, status

# User creation
def create_user(db: Session, user_input: UserInput) -> User:
    # Check if username already exists
    existing_user_by_username = db.query(User).filter(User.username == user_input.username).first()
    if existing_user_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists.")

    # Check if email already exists
    existing_user_by_email = db.query(User).filter(User.email == user_input.email).first()
    if existing_user_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")

    # If validation passes, create the user
    user = User(
        username=user_input.username,
        email=user_input.email,
        hashed_password=get_password_hash(user_input.password)
    )

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
    
# Authenticate user, returning a valid access token, if possible
def authenticate(db: Session, user_login: UserLogin) -> str:
    user = get_user_by_email(db, user_login.email)
    if not user:
        raise ValueError('The email is not associated to any account.')
    if not verify_password(user_login.password, user.hashed_password):
        raise ValueError('Incorrect password.')
    
    return create_access_token(user.id)
