import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import User, UserInput
from crud.user import create_user, get_user_by_username, get_user_by_email, get_user_by_id
from core.config import Base
from tests.utils import random_lower_string, random_email
from core.security import get_password_hash, verify_password

# Setting up the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # Use in-memory SQLite for testing
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize the database
Base.metadata.create_all(bind=engine)

# Dependency override for the test session
@pytest.fixture
def db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test utils
def test_utils():
    username = random_lower_string()
    email = random_email()
    password = random_lower_string()
    hashed_password = get_password_hash(password)

    assert len(username) == 32
    assert len(email) == 69
    assert len(password) == 32
    assert verify_password(password, hashed_password)
    
# Test user creation
def test_create_user(db):
    email = random_email()
    username = random_lower_string()
    password = random_lower_string()

    user_input = UserInput(username=username, email=email, password=password)
    user = create_user(db, user_input)

    assert user.username == username
    assert user.email == email
    assert user.hashed_password != password  # Should be hashed

# Test getting user by username
def test_get_user_by_username(db):
    username = random_lower_string()
    user_input = UserInput(username=username, email=random_email(), password=random_lower_string())
    create_user(db, user_input)

    user = get_user_by_username(db, username)
    assert user
    assert user.username == username

# Test getting user by email
def test_get_user_by_email(db):
    email = random_email()
    user_input = UserInput(username=random_lower_string(), email=email, password=random_lower_string())
    create_user(db, user_input)

    user = get_user_by_email(db, email)
    assert user
    assert user.email == email

# Test getting user by id
def test_get_user_by_id(db):
    user_input = UserInput(username=random_lower_string(), email=random_email(), password=random_lower_string())
    user = create_user(db, user_input)

    fetched_user = get_user_by_id(db, user.id)
    assert fetched_user
    assert fetched_user.id == user.id
