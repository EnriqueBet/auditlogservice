import config

from fastapi import FastAPI
from pymongo import MongoClient
from db import router

app = FastAPI()

@app.on_event("startup")
def _initialize_db_client():
    app.mongodb_client = MongoClient(host=config.MONGO_CLIENT_URL)
    app.database = app.mongodb_client[config.MONGO_DB_NAME]

@app.on_event('shutdown')
def _shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router, tags=['events'], prefix="/events")