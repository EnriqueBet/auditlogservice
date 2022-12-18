import os

from typing import List
from fastapi import status, Request, Response, APIRouter
from fastapi.encoders import jsonable_encoder

from models import LogEvent, LogEventRead
from utils import date_format_validator
from exceptions import IncorrectDateFormatError

DATABASE_URL = os.getenv('DATABASE_URL')
router = APIRouter()

@router.post("/", 
             response_description="Create a new log event",
             status_code=status.HTTP_201_CREATED,
             response_model=LogEvent)
def create_events(request: Request, event: LogEvent):
    event = jsonable_encoder(event)
    new_event = request.app.database["events"].insert_one(event)
    created_event = request.app.database["events"].find_one({"_id": new_event.inderted_id})
    return created_event

@router.get("/",
            response_description="List al events",
            response_model=List[LogEventRead]
            )
def list_events(request: Request):
    params = request.query_params()
    query = {"limit": 100}

    # Validate data formatting
    if "start_date" in params:
        if not date_format_validator(params["start_date"]):
            return IncorrectDateFormatError(key='start_date')
        query["timestamp"] = {'$gte': params["start_date"]}
    
    if "end_date" in params:
        if not date_format_validator(params["end_date"]):
            return IncorrectDateFormatError(key='end_date')
        query["timestamp"] = {'$lt': params["end_date"]}
    
    for param, value in params.items():
        if param not in ('start_date', 'end_date', 'data'):
            query[param] = value
    return request.app.database["events"].find(query)
    