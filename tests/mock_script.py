import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1.utils import common
from api.v1.database import DatabaseClient as db


def mock_create_user(username: str, password: str):
    """Registers a user to the service for testing purposes

    :param username: Username
    :param password: Password
    """
    result = db.get_instance().database["users"].insert_one({
                                                "username": username,
                                                "hashed_password": common.encrypt_password(password).decode(),
                                                "disabled": False
                                             })
    print(db.get_instance().database["users"].find_one({"_id": result.inserted_id}))

mock_create_user("ijansky", "1234568694")
mock_create_user("frankban", "1234566234")
