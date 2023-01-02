import bcrypt
import v1.config as config

from jose import jwt
from datetime import datetime, timedelta

def encrypt_password(pwd: str):
    """Encrypts a password using satls to avoid rainbow table attacks

    :param pwd: The password to be encrypted
    :return: Hashed password with random salt
    """
    return bcrypt.hashpw(pwd.encode(), bcrypt.gensalt())

def create_access_token(data: dict, expiration: timedelta | None = None):
    data_clone = data.copy()
    expire = datetime.utcnow() + (expiration if expiration else timedelta(minutes=config.ACCESS_TOKEN_EXPIRATION))
    data_clone.update({"exp": expire})
    return jwt.encode(data_clone, key=config.SECRET_KEY, algorithm=config.HASH_ALGO)
