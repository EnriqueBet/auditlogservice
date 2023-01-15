import os

# MONGO CLIENT URL
MONGO_CLIENT_URL = os.getenv("MONGO_CLIENT_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "auditlogservice")

# EVENTS DEFAULTS
EVENT_QUERY_DEFAULT_LIMIT = int(os.getenv("EVENT_QUERY_DEFAULT_LIMIT", 100))

# Application configuration
SERVICE_BASE_URL = os.getenv("SERVICE_BASE_URL", "http://0.0.0.0")
SERVICE_PORT = os.getenv("SERVICE_PORT", "8080")
DEFAULT_SECRET_KEY = "f03970f3989ab8833e78479e47ded5aa62d745640495c930c6b692464dec0c9f" # Warning!!: Secret key must be changed for production!!
SECRET_KEY = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)
HASH_ALGO = os.getenv("HASH_ALGO", "HS256")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")

# Token expiration in minutes
ACCESS_TOKEN_EXPIRATION = os.getenv("TOKEN_DEFAULT_EXPIRTATION", 60*12)
