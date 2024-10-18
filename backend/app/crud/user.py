""" User related CRUD methods """
from sqlalchemy.orm import Session
from core.models import User, UserInput
from core.security import get_password_hash

# User creation
def create_user(db: Session, user_input: UserInput) -> User:
    db_user = User.model_validate(
        user_input, update={"hashed_password": get_password_hash(user_input.password)}
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
