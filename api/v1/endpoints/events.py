from datetime import datetime
from typing import List

import pytz
from bson import ObjectId
from fastapi import (APIRouter, Depends, HTTPException, Request, Response,
                     status)
from fastapi.encoders import jsonable_encoder

from api.v1 import config
from api.v1.endpoints.users import get_current_user
from api.v1.models import LogEvent, StoredLogEvent, User

router = APIRouter()

@router.post("/", 
             response_description="Log an event",
             status_code=status.HTTP_201_CREATED,
             response_model=StoredLogEvent)
async def create_events(request: Request, event: LogEvent, user: User = Depends(get_current_user)):
    event = jsonable_encoder(event)

    # Set server sources and timestamp
    event["user_id"] = user.id
    event["timestamp"] = datetime.now(pytz.utc)
    event["source"] = request.client[0]

    # Insert a new event into the database
    new_event = request.app.database["events"].insert_one(event)
    created_event = request.app.database["events"].find_one({"_id": new_event.inserted_id})
    print(created_event)
    print(request.app.database.list_collection_names())
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
        for param in str(request.query_params).split("&"):
            key, value = param.split("=")
            params[key] = ObjectId(value) if key.startswith("_id") or key.endswith("_id") else value
    
    return list(request.app.database["events"].find(params, limit=config.EVENT_QUERY_DEFAULT_LIMIT))

@router.get("/{id}",
            response_description="Retrieve a single event using id",
            response_model=LogEvent)
async def find_event(id: str, request: Request, user: User = Depends(get_current_user)):
    query = request.app.database["events"].find_one({"_id": ObjectId(id)})
    if (event := request.app.database["events"].find_one({"_id": ObjectId(id)})):
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")

@router.delete("/{id}",
               response_description="Detele a single event by id",
               response_model=LogEvent)
async def delete_event(id: str, request: Request, 
                 response: Response, user: User = Depends(get_current_user)) -> Response:
    deletion_result = request.app.database["events"].delete_one({"_id": ObjectId(id)})
    if deletion_result.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")
