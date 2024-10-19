from core.config import get_db
from core.models import UserInput
from core.security import get_password_hash, verify_password
from crud.user import create_user
from tests.utils import random_lower_string, random_email

def test_utils():
    # Random username, email and password
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    hash_pwd = get_password_hash(pwd)

    # Check data
    assert len(username) == 32
    assert len(email) == 69
    assert len(pwd) == 32
    assert verify_password(pwd, hash_pwd)

def test_create_user():
    # Get database session
    db = next(get_db())

    # Create random user
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    user_input = UserInput(username=username, email=email, password=pwd)
    user = create_user(db, user_input)

    # Check object created
    assert user is not None
    assert user.username == username
    assert user.email == email
    assert verify_password(pwd, user.hashed_password)

    # Remove data created
    db.delete(user)
    db.commit()
