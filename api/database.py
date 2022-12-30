import config
from pymongo import MongoClient

class DatabaseClient:
    host = config.MONGO_CLIENT_URL
    database_name = config.MONGO_DB_NAME
    _instance = None

    @staticmethod
    def get_instance():
        if not __class__._instance:
            __class__._instance = MongoClient(host=__class__.host)
        return __class__._instance

    def __call__(self):
        return __class__.get_instance()
