""" User related CRUD methods """
from sqlalchemy.orm import Session
from core.models import User, UserInput
from core.security import get_password_hash

# User creation
def create_user(db: Session, user_input: UserInput) -> User:
    user = User(username=user_input.username, email=user_input.email,
                hashed_password = get_password_hash(user_input.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
