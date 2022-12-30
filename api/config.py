import os

# MONGO CLIENT URL
MONGO_CLIENT_URL = os.getenv("MONGO_CLIENT_URL")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

# EVENTS DEFAULTS
EVENT_QUERY_DEFAULT_LIMIT = int(os.getenv("EVENT_QUERY_DEFAULT_LIMIT", 100))

# Application configuration
SECRET_KEY = os.getenv("AUDIT_LOG_SERVICE_SECRET_KEY")
HASH_ALGO = os.getenv("AUDIT_LOG_SERVICE_HASH_ALGO", "HS256")

# Token expiration in minutes
ACCESS_TOKEN_EXPIRATION = os.getenv("ACCESS_TOKEN_EXPIRTATION")
