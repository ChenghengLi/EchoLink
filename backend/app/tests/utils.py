import random
import string
from models.user import UserInput
from crud.user import create_user

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