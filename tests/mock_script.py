from v1.utils import encrypt_password
from v1.database import DatabaseClient

def mock_create_user(username: str, password: str):
    """Creates users only for testing purposes"""
    salted_password = encrypt_password(password)
    DatabaseClient.get_instance().database['users'].insert_one({"username": username, "hashed_password": salted_password.decode(), "disabled": False})
    query = list(DatabaseClient.get_instance().database['users'].find({"username": username}))
    print(query)


mock_create_user("enrique", "123562432")
