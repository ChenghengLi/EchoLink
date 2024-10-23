import pytest
from core.config import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User, UserInput
from crud.user import create_user, get_user_by_username, get_user_by_email, get_user_by_id
from core.config import Base
from tests.utils import random_lower_string, random_email
from core.security import get_password_hash, verify_password
from fastapi import HTTPException, status

# Function to create a random user
def create_random_user():
    # Get database session
    db = next(get_db())

    # Create random user
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    user_input = UserInput(username=username, email=email, password=pwd)
    user = create_user(db, user_input)

    return db, user

# Test getting user by username
def test_get_user_by_username():
    db, user = create_random_user()

    # Get user by username
    db_user = get_user_by_username(db, user.username)

    # Check user is the same
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.hashed_password == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

# Test getting user by email
def test_get_user_by_email():
    db, user = create_random_user()

    # Get user by email
    db_user = get_user_by_email(db, user.email)

    # Check user is the same
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.hashed_password == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

# Test getting user by id
def test_get_user_by_id():
    db, user = create_random_user()

    # Get user by id
    db_user = get_user_by_id(db, user.id)

    # Check user is the same
    assert db_user is not None
    assert db_user.username == user.username
    assert db_user.email == user.email
    assert db_user.hashed_password == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

# Test invalid username (less than 4 characters)
def test_create_user_invalid_username():
    db = next(get_db())

    # Username that doesn't meet the regex requirements
    with pytest.raises(ValueError):
        user_input = UserInput(username="abc", email="test@example.com", password="strongpassword")
        create_user(db, user_input)

# Test invalid email format
def test_create_user_invalid_email():
    db = next(get_db())
    
    with pytest.raises(ValueError):
        # Invalid email format
        user_input = UserInput(username="validuser", email="notanemail", password="strongpassword")
        create_user(db, user_input)


# Test unique username constraint
def test_create_user_duplicate_username():
    db, user = create_random_user()

    # Attempt to create another user with the same username
    user_input = UserInput(username=user.username, email="newemail@example.com", password="newpassword")

    with pytest.raises(HTTPException) as exc_info:
        create_user(db, user_input)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Username already exists."

# Test unique email constraint
def test_create_user_duplicate_email():
    db, user = create_random_user()

    # Attempt to create another user with the same email
    user_input = UserInput(username="newuser", email=user.email, password="newpassword")

    with pytest.raises(HTTPException) as exc_info:
        create_user(db, user_input)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Email already exists."
