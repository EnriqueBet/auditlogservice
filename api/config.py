import os

# MONGO CLIENT URL
MONGO_CLIENT_URL = os.getenv("MONGO_CLIENT_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# EVENTS DEFAULTS
EVENT_QUERY_DEFAULT_LIMIT = int(os.getenv("EVENT_QUERY_DEFAULT_LIMIT", 100))

# Application configuration
DEFAULT_SECRET_KEY = "f03970f3989ab8833e78479e47ded5aa62d745640495c930c6b692464dec0c9f" # Warning!!: Secret key must be changed for production!!
SECRET_KEY = os.getenv("AUDIT_LOG_SERVICE_SECRET_KEY", DEFAULT_SECRET_KEY)
HASH_ALGO = os.getenv("AUDIT_LOG_SERVICE_HASH_ALGO", "HS256")

# Token expiration in minutes
ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRTATION")
