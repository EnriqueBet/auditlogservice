import os
import sys
import pytz
import string
import requests
import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1 import config
from api.v1.utils import common
from api.v1.database import DatabaseClient as db
from api.v1.utils.logger import Logger
from random import choice

logger = Logger.get_instance()
TEXT_POOL = string.ascii_letters + string.digits + string.punctuation

def create_test_user():
    """Create a user for testing purposed

    :raises Exception: raised if the user was not created
    :return: a dictionary containing the test user information
    """
    # Define test user credentials
    username = f"test-{random_text(chars=string.ascii_letters)}"
    password = ''.join(random_text(length=12))

    # Attempt to create test user
    logger.info(f"Creating test user: {username}...")
    result = db.get_instance().database["users"].insert_one({
        "username": username,
        "hashed_password": common.encrypt_password(password).decode(),
        "disabled": False
    })

    # Verify that the test user was created
    created_user = db.get_instance().database["users"].find_one({"_id": result.inserted_id})
    if not created_user:
        logger.error("The test user wasn't created, cannot proceed with the test")
        raise Exception("The test user wasn't created, cannot proceed with the test")
    created_user["password"] = password
    logger.info(f"Test user {username} was successfully created!")
    return created_user

def login(username: str, password: str):
    """Login to the API with a given user and password
    
    :param username: username for the registered user
    :param password: password for the registered user
    :raises Exception: raised if user was not created
    :return: Dictionary containing 'authorization_token' and 'authorization_type'
    """
    logger.info(f"Attempting to login with test user: {username}")
    url = f"{config.SERVICE_BASE_URL}:{config.SERVICE_PORT}/token"
    headers = {
        "Content-": "form-data"
    }
    body = {
        "username": (None, username),
        "password": (None, password)
    }
    response = requests.post(url=url, headers=headers, files=body)
    if response.status_code != 200:
        logger.error(f"Unable to create user. Status Code: {response.status_code} Msg: {response.content}")
        raise Exception(f"Unable to create user. Status Code: {response.status_code} Msg: {response.content}")
    logger.info(f"Successfully logged in with user: {username}")
    return response.json()
    

def delete_user(id: str) -> bool:
    """Deletes the given user

    :param id: The id of the user to delete
    :return: True if the user was deleted, otherwise, False
    """
    logger.info(f"Attempting to delete user with id: {id}")
    result = db.get_instance().database["users"].delete_one({"_id": id})
    if not result.deleted_count:
        logger.warning(f"An error ocurred while deleting user with id: {id}")
        return False
    logger.info(f"Successfully deleted user with id: {id}")
    return True
    

def random_text(chars: str = TEXT_POOL, length: int = 6) -> str:
    """Generates random text from a given text list and length

    :param chars: a string filled with characters
    :param length: the lenght of the text output, defaults to 6
    :return: random string of fixed length
    """
    return "".join(choice(chars) for _ in range(length))

def create_an_event():
    """Warning!!! This method is only meant to be used for testing
    Creates an event directly on the database

    :raises Exception: raised if event was not created
    :return: a dictionary containing the information from a created event
    """
    # Create an event on the database
    result = db.get_db()["events"].insert_one(
        {
            "name": f'TestFetchEvent-{random_text(length=6)}',
            "detail": f'TestDetail-{random_text(length=12)}',
            'event_type': 'TestEventType',
            'timestamp': str(datetime.datetime.now(pytz.utc))
        }
    )
    if not (event := db.get_db()['events'].find_one({"_id": result.inserted_id})):
        logger.error("An error ocurred while attempting to create event...")
        raise Exception("An error ocurred while attempting to create event...")
    return event
