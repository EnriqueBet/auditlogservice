import requests
import string

from api.v1 import config as config
from api.v1.database import DatabaseClient as db
from random import choice

TEXT_POOL = string.ascii_letters + string.digits + string.punctuation

def create_test_user():
    username = f"test-{random_text(string.ascii_letters)}"
    password = ''.join(random_text(12))
    result_id = db.database["users"].insert_one({
        "usename": username,
        "password": password,
        "disable": False
    })
    created_user = db.database["users"].find_one({"_id": result_id})
    if not created_user:
        raise Exception("The test user wasn't created, cannot proceed with the test")
    created_user["password"] = password
    return created_user

def login(username: str, password: str):
    headers = {
        "Content-Type": "text/json"
    }

    body = {
        "username": username,
        "password": password
    }

    result = requests.post(url=config.SERVICE_URL, 
                           headers=headers,
                           body=body)

    return result.json()
    

def delete_user(id: str) -> bool:
    """Deletes the given user

    :param id: The id of the user to delete
    :returns: True if the user was deleted, otherwise, False
    """
    return db.database["users"].delete_one({"_id": id})
    

def random_text(text_map: str, length: int = 6) -> str:
    text_map = TEXT_POOL if not text_map else text_map
    return "".join(choice(string.ascii_letters + string.digits) for _ in range(length))
