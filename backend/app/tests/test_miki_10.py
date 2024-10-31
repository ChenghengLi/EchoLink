from core.config import get_db
from models.user import User, UserInput
from crud.user import create_user
from tests.utils import random_lower_string, random_email
from fastapi.testclient import TestClient
from main import app
from core.security import verify_password

client = TestClient(app)

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

def test_create_correct_user():
    db = next(get_db())

    # Create a valid user
    new_username = random_lower_string()
    new_email = random_email()
    new_password = random_lower_string()

    response = client.post("/users/user", json={"username": new_username, "email": new_email, "password": new_password})

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == new_username
    assert response.json()['email'] == new_email
    assert verify_password(new_password, response.json()['hashed_password'])

    # Remove data created
    db_user = db.query(User).filter(User.username == new_username).first()
    db.delete(db_user)
    db.commit()

    # Check the user is no longer in db
    db_user = db.query(User).filter(User.username == new_username).first()
    assert db_user is None


def test_get_user_by_id():
    db, user = create_random_user()

    # Get user by id
    response = client.get(f"/users/get_user/{user.id}")

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == user.username
    assert response.json()['email'] == user.email
    assert response.json()['hashed_password'] == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

def test_get_user_by_username():
    db, user = create_random_user()

    # Get user by username
    response = client.get(f"/users/get_user_by_username/{user.username}")

    # Check object returned
    assert response.status_code == 200
    assert response.json()['username'] == user.username
    assert response.json()['hashed_password'] == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

def test_get_user_by_email():
    db, user = create_random_user()

    # Get user by email
    response = client.get(f"/users/get_user_by_email/{user.email}")

    # Check object returned
    assert response.status_code == 200
    assert response.json()['email'] == user.email
    assert response.json()['hashed_password'] == user.hashed_password

    # Remove data created
    db.delete(user)
    db.commit()

def test_create_user_duplicate_email():
    db, user = create_random_user()

    # Create a new user
    response = client.post("/users/user", json={"username": "new_username", "email": user.email, "password": "123456"})

    # Check object returned
    assert response.status_code == 400
    assert response.json()['detail'] == "Email already registered"

    # Remove data created
    db.delete(user)
    db.commit()

def test_create_user_duplicate_username():
    db, user = create_random_user()

    # Create a new user with a valid email format
    response = client.post("/users/user", json={"username": user.username, "email": "email_testing@example.com", "password": "123456"})

    # Check object returned
    assert response.status_code == 400
    assert response.json()['detail'] == "Username already registered"

    # Remove data created
    db.delete(user)
    db.commit()

def test_create_user_invalid_email():
    db, user = create_random_user()

    # Create a new user with an invalid email format
    response = client.post("/users/user", json={"username": "new_username", "email": "invalid_email", "password": "123456"})

    # Check object returned
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Incorrect email format."

    # Remove data created
    db.delete(user)
    db.commit()

def test_create_user_invalid_username():
    db, user = create_random_user()

    # Create a new user with an invalid username format
    response = client.post("/users/user", json={"username": "inv", "email": "email_testing@example.com", "password":"123456"})

    # Check object returned
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Value error, Username must be 4-16 characters long, containing only letters, numbers, and underscores."

    # Remove data created
    db.delete(user)
    db.commit()


