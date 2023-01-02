import v1.config as config

from fastapi import FastAPI
from v1.database import DatabaseClient
from v1.api import router

app = FastAPI()

@app.on_event("startup")
def _initialize_db_client():
    app.mongodb_client = DatabaseClient.get_instance()
    app.database = app.mongodb_client[config.MONGO_DB_NAME]

@app.on_event('shutdown')
def _shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router)
