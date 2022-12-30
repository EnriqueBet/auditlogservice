import bcrypt
import config

from jose import jwt

from models import User
from datetime import datetime, timedelta

def date_format_validator(input_date) -> bool:
    # TODO create this function to actually return the error
    if input_date is None:
        return False
    if not isinstance(input_date, datetime):
        return False
    return True

def decode_token(token: str):
    return  User(username=f"MockToken {token}",
                email="mockmail@example.com",
                full_name="Juan Perez")

def encrypt_password(pwd: str):
    """Encrypts a password using satls to avoid rainbow table attacks

    :param pwd: The password to be encrypted
    :return: Hashed password with random salt
    """
    return bcrypt(pwd.encode(), bcrypt.gensalt())

def create_access_token(data: dict, expiration: timedelta | None = None):
    data_clone = data.copy()
    expire = datetime.utcnow() + (expiration if expiration else timedelta(minutes=config.DEFAULT_EXPIRATION))
    data_clone.update({"exp": expire})
    return jwt.encode(data_clone, secret_key=config.SECRET_KEY, algorithm=config.HASH_ALGO)
