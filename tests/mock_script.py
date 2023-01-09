import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1 import utils
from api.v1.database import DatabaseClient as db


def mock_create_user(username: str, password: str):
    """Creates users only for testing purposes"""
    salted_password = utils.encrypt_password(password)
    db.get_instance().database['users'].insert_one({"username": username, "hashed_password": salted_password.decode(), "disabled": False})
    query = list(db.get_instance().database['users'].find({"username": username}))
    print(query)

mock_create_user("enrique", "123562432")
