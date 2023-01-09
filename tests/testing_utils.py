import os
import sys
import string
import requests

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1 import config
from api.v1 import utils
from api.v1.database import DatabaseClient as db
from random import choice

TEXT_POOL = string.ascii_letters + string.digits + string.punctuation

def create_test_user():
    username = f"test-{random_text(string.ascii_letters)}"
    password = ''.join(random_text(12))
    result = db.get_instance().database["users"].insert_one({
        "username": username,
        "hashed_password": utils.encrypt_password(password).decode(),
        "disabled": False
    })
    created_user = db.get_instance().database["users"].find_one({"_id": result.inserted_id})
    if not created_user:
        raise Exception("The test user wasn't created, cannot proceed with the test")
    created_user["password"] = password
    return created_user

def login(username: str, password: str):

    url = f"{config.SERVICE_BASE_URL}:{config.SERVICE_PORT}/token"
    headers = {
        "Content-": "form-data"
    }
    body = {
        "username": (None, username),
        "password": (None, password)
    }

    response = requests.post(url=url, 
                           headers=headers, files=body)
    return response.json()
    

def delete_user(id: str) -> bool:
    """Deletes the given user

    :param id: The id of the user to delete
    :returns: True if the user was deleted, otherwise, False
    """
    return db.get_instance().database["users"].delete_one({"_id": id})
    

def random_text(text_map: str, length: int = 6) -> str:
    text_map = TEXT_POOL if not text_map else text_map
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))
