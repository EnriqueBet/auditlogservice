import sys, os, getpass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from api.v1.utils import common
from api.v1.utils.logger import Logger
from api.v1.database import DatabaseClient as db

logger = Logger().get_instance()

def mock_create_user():
    """Registers a user to the service for testing purposes

    :param username: Username
    :param password: Password
    """
    username = input("Please type your usename:\n > ")
    password = getpass.getpass("Please type your password:\n > ")
    password_confirm = getpass.getpass("Please confirm your password:\n > ")

    if password != password_confirm:
        logger.error("your passwords doesn't match!! Please try again!")
        raise Exception("your passwords doesn't match!! Please try again!")

    result = db.get_instance().database["users"].insert_one({
                                                "username": username,
                                                "hashed_password": common.encrypt_password(password).decode(),
                                                "disabled": False
                                             })
    if result:
        logger.info(f"Successfully created test user: {username}")
        return
    
    logger.error(f'An error ocurred while creating user: {username}')
    

if __name__ == "__main__":
    mock_create_user()

