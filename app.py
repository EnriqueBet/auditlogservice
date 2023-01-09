from fastapi import FastAPI
from api.v1 import config
from api.v1.api import router
from api.v1.database import DatabaseClient

app = FastAPI()

@app.on_event("startup")
def _initialize_db_client():
    app.mongodb_client = DatabaseClient.get_instance()
    app.database = DatabaseClient.get_db()

@app.on_event('shutdown')
def _shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router)
