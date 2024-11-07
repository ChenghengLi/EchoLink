from core.config import get_db
from models.user import UserInput
from crud.user import create_user
from tests.utils import random_lower_string, random_email
from fastapi.testclient import TestClient
from main import app

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

def test_get_user_by_username():
    # Create a random user and save it to the database
    db, user = create_random_user()

    # Make a GET request to fetch the user by username
    response = client.get(f"/users/username?username={user.username}")

    # Check that the response is successful and returns the correct data
    assert response.status_code == 200
    assert response.json()['username'] == user.username
    assert response.json()['email'] == user.email

    # Clean up by deleting the test user from the database
    db.delete(user)
    db.commit()

def test_get_user_by_username_not_found():
    # Generate a random username that doesn't exist
    non_existent_username = random_lower_string()

    # Make a GET request to fetch a user that doesn't exist
    response = client.get(f"/users/username?username={non_existent_username}")

    # Check that the response status is 404 and the appropriate error message is returned
    assert response.status_code == 404
    assert response.json()['detail'] == "User not found"
