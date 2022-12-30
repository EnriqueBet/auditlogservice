import config

from fastapi import FastAPI

from events import router as event_router
from users import router as user_router
from database import DatabaseClient

app = FastAPI()

@app.on_event("startup")
def _initialize_db_client():
    app.mongodb_client = DatabaseClient.get_instance()
    app.database = app.mongodb_client[config.MONGO_DB_NAME]

@app.on_event('shutdown')
def _shutdown_db_client():
    app.mongodb_client.close()

app.include_router(user_router, tags=["token"], prefix="/token")
app.include_router(event_router, tags=['events'], prefix="/events")
