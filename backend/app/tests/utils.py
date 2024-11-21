import random
import string
from core.config import get_db
from main import app
from fastapi.testclient import TestClient
from models.user import UserInput, UserLogin
from models.artist import ArtistInput
from models.listener import ListenerInput
from crud.user import authenticate, create_user
from crud.artist import create_artist
from crud.listener import create_listener

def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=10))

def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"

def create_random_user_input():
    username = random_lower_string()
    email = random_email()
    pwd = random_lower_string()
    return UserInput(username=username, email=email, password=pwd)

def create_random_user(db):
    return create_user(db, create_random_user_input())

def create_random_auth_user(db):
    user_input = create_random_user_input()
    user = create_user(db, user_input)
    authenticate(db, UserLogin(email=user_input.email, password=user_input.password))
    db.refresh(user)
    return user

def get_session():
    return next(get_db())

def get_client():
    return TestClient(app)

def make_artist(db, user):
    artist_input = ArtistInput(username=user.username, name=random_lower_string(), genre=random_lower_string(), bio=random_lower_string())
    return create_artist(db, artist_input)

def make_listener(db, user):
    listener_input = ListenerInput(username=user.username)
    return create_listener(db, listener_input)

def create_random_artist(db):
    return make_artist(db, create_random_user(db))

def create_random_listener(db):
    return make_listener(db, create_random_user(db))

