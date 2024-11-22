from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.listener import Listener
from models.user import User

# Get listener by user_id
def get_listener_by_user_id(db: Session, user_id: int) -> Listener:
    return db.query(Listener).filter(Listener.user_id == user_id).first()

# Create listener
def create_listener(db: Session, user: User) -> Listener:
    # Check if a listener already exists for this user
    if get_listener_by_user_id(db, user.id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is already a listener.")

    # Create a new listener
    listener = Listener(user_id=user.id)

    # Save to the database
    db.add(listener)
    db.commit()
    db.refresh(listener)

    return listener

# Get listener by username
def get_listener_by_username(db: Session, username: str) -> Listener:
    # Get user by username
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Get listener by user_id
    listener = get_listener_by_user_id(db, user.id)
    if not listener:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This user is not a listener.")
    
    return listener
