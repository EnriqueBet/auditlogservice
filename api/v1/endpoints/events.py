import pytz
import urllib.parse

from typing import List
from datetime import datetime
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.encoders import jsonable_encoder

from api.v1 import config
from api.v1.endpoints.users import get_current_user
from api.v1.models import LogEvent, StoredLogEvent, User
from api.v1.utils.logger import Logger

router = APIRouter()
logger = Logger.get_instance()

@router.post("/", 
             response_description="Log an event",
             status_code=status.HTTP_201_CREATED,
             response_model=StoredLogEvent)
async def create_event(request: Request, event: LogEvent, user: User = Depends(get_current_user)):
    """REST endpoint to create an event

    :param request: client request object
    :param event: object model parsed from the request body
    :param user: fixes a dependency on logged users to use this method, defaults to Depends(get_current_user)
    :return: a dictionary containing the information fromr the created event
    """
    # Pass the received body to a dictionary
    event = jsonable_encoder(event)
    logger.info(f"Creating an event with name: {event['name']} from user: {user.id}")

    # Set server sources and timestamp
    event["user_id"] = user.id
    event["timestamp"] = datetime.now(pytz.utc)
    event["source"] = request.client[0]

    # Insert a new event into the database
    new_event = request.app.database["events"].insert_one(event)
    if not (created_event := request.app.database["events"].find_one({"_id": new_event.inserted_id})):
        logger.error(f"An error ocurred while creating the event: {new_event['name']}")
        raise HTTPException(status_code=500, 
                            detail=f"An error ocurred while creating the event: {new_event['name']}")
    logger.info(f"Event {event['name']} was successfully created by user: {user.id}!!")
    return created_event

@router.get("/",
            response_description="Retrieve a list of logged events",
            response_model=List[StoredLogEvent]
            )
async def get_events(request: Request, user: User = Depends(get_current_user)):
    """
    Get a list of events from a given user

    :param: 
    """
    # TODO: Set correct permissions for users based on their scope
    params = {}
    if request.query_params:
        params = urllib.parse.parse_qs(str(request.query_params))
        # Added '$in' keyword to use multiple field/value query
        params = {key: {"$in": value} for key, value in params.items()}
    
    return list(request.app.database["events"].find(params, limit=config.EVENT_QUERY_DEFAULT_LIMIT))

@router.get("/{id}",
            response_description="Retrieve a single event using id",
            response_model=LogEvent)
async def find_event(id: str, request: Request, user: User = Depends(get_current_user)):
    if (event := request.app.database["events"].find_one({"_id": id})):
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")

@router.delete("/{id}",
               response_description="Detele a single event by id",
               response_model=LogEvent)
async def delete_event(id: str, request: Request, 
                 response: Response, user: User = Depends(get_current_user)) -> Response:
    deletion_result = request.app.database["events"].delete_one({"_id": id})
    if deletion_result.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")
