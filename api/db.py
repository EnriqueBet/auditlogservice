import pytz
import config

from typing import List
from datetime import datetime
from fastapi import status, Request, Response, APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from utils import date_format_validator
from models import LogEvent, LogEventRead
from exceptions import IncorrectDateFormatError

router = APIRouter()

@router.post("/", 
             response_description="Create a new log event",
             status_code=status.HTTP_201_CREATED,
             response_model=LogEvent)
def create_events(request: Request, event: LogEvent):
    event = jsonable_encoder(event)

    # Set server sources and timestamp
    event["timestamp"] = datetime.now(pytz.utc)
    event["source"] = request.client[0]

    # Insert a new event into the database
    new_event = request.app.database["events"].insert_one(event)
    created_event = request.app.database["events"].find_one({"_id": new_event.inserted_id})
    return created_event

@router.get("/",
            response_description="List al events",
            response_model=List[LogEvent]
            )
def get_events(request: Request):
    params = request.query_params
    print(params)
    query = {}

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

    return list(request.app.database["events"].find(query, limit=config.EVENT_QUERY_DEFAULT_LIMIT))

@router.get("/{id}",
            response_description="Get a single event by id",
            response_model=LogEvent)
def find_event(id: str, request: Request):
    if (event := request.app.database["events"].find_one({"_id": id})):
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")

@router.delete("/{id}",
               response_description="Detele a single event by id",
               response_model=LogEvent)
def delete_event(id: str, request: Request, response: Response) -> Response:
    deletion_result = request.app.database["events"].delete_one({"_id": id})
    if deletion_result.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")
