import config

from fastapi import FastAPI
from api.routes import router
from database import DatabaseClient

app = FastAPI()

@app.on_event("startup")
def _initialize_db_client():
    app.mongodb_client = DatabaseClient()
    app.database = app.mongodb_client[DatabaseClient.database_name]

@app.on_event('shutdown')
def _shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router, tags=['events'], prefix="/events")
