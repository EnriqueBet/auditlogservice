import requests
from api.v1 import config as config
from api.v1.database import DatabaseClient as db



def create_test_user():
    username = "test-user"
    password = "12345678910"
    result_id = db.database["users"].insert_one({
        "usename": username,
        "password": password,
        "disable": False
    })
    created_user = db.database["users"].find_one({"_id": result_id})
    return bool(created_user)

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

    return result
    