import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1.utils import common
from api.v1.database import DatabaseClient as db
from tests import testing_utils


def mock_create_user(username: str, password: str):
    """Registers a user to the service for testing purposes

    :param username: Username
    :param password: Password
    """
    salted_password = common.encrypt_password(password)
    result = db.get_instance().database['users'].insert_one({
                                                             "username": username, 
                                                             "hashed_password": salted_password.decode(), 
                                                             "disabled": False
                                                             })
    if not (db.get_instance().database['users'].find_one({"_id": result.inserted_id})):
        raise Exception("The test user was not created")

print(testing_utils.create_test_user())
