from utils import encrypt_password
from database import DatabaseClient
import bcrypt

def mock_create_user(username: str, password: str):
    """Creates users only for testing purposes"""
    salted_password = encrypt_password(password)
    print(salted_password)
    DatabaseClient.get_instance().database['users'].insert_one({"username": username, "password": salted_password})
    print(bcrypt.checkpw(password.encode(), salted_password))
    query = list(DatabaseClient.get_instance().database['users'].find({"username": username}))
    print(query)


mock_create_user("enrique", "123562432")
