from api.v1 import config
from pymongo import MongoClient

class DatabaseClient:
    host = config.MONGO_CLIENT_URL
    database_name = config.MONGO_DB_NAME
    _instance = None
    _database = None

    @staticmethod
    def get_instance():
        if not __class__._instance:
            __class__._instance = MongoClient(host=__class__.host)

        return __class__._instance

    @staticmethod
    def get_db():
        if __class__._database is None:
            __class__._database = __class__.get_instance()[__class__.database_name]

        return __class__._database

    def __call__(self):
        return __class__.get_instance()
