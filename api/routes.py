import pytz
import config

from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import status, Request, Response, APIRouter, HTTPException, Depends

from models import LogEvent, RegisteredUser, TokenData, Token, User
from database import DatabaseClient as db_client
from utils import date_format_validator, create_access_token
from exceptions import IncorrectDateFormatError

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="authToken")
pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def verify_password(str_pwd: str, hash_pwd: str) -> bool:
    return pwd_context.verify(str_pwd, hash_pwd)

def get_pwd_hash(pwd):
    return pwd_context.hash(pwd)

def authenticate_user(username: str, pwd: str):
    user = get_user(username)
    if not user or not verify_password(pwd, user.hashed_password):
        return False
    return user

def get_user(username: str):
    user_map = db_client.get_instance().database["users"].find_one({'username': username})
    if user_map:
        return RegisteredUser(**user_map)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials were not validated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=config.HASH_ALGO)
        if username := str(payload.get("sub")) is None:
            raise user_exception
        token_data = TokenData(username=username)
    except JWTError as error:
        raise user_exception
    if user := get_user(username=token_data.username) is None:
        raise user_exception
    
    if user.is_disabled:
        raise HTTPException(status_code=400, detail='Your user is disabled, please contact the system admin')
    return user

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not (user := authenticate_user(form_data.username, form_data.password)):
        raise HTTPException(status_code=400, 
                            detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=config.ACCESS_TOKEN_EXPIRATION
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", 
             response_description="Create a new log event",
             status_code=status.HTTP_201_CREATED,
             response_model=LogEvent)
async def create_events(request: Request, event: LogEvent, user: User = Depends(get_current_user)):
    event = jsonable_encoder(event)

    # Set server sources and timestamp
    event["user"] = user
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
async def get_events(request: Request, token: str=Depends(get_current_user)):
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

    return list(request.app.database["events"].find(query, 
                                                    limit=config.EVENT_QUERY_DEFAULT_LIMIT))

@router.get("/{id}",
            response_description="Get a single event by id",
            response_model=LogEvent)
async def find_event(id: str, request: Request, token: str=Depends(get_current_user)):
    if (event := request.app.database["events"].find_one({"_id": id})):
        return event
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")

@router.delete("/{id}",
               response_description="Detele a single event by id",
               response_model=LogEvent)
async def delete_event(id: str, request: Request, 
                 response: Response, token: str=Depends(get_current_user)) -> Response:
    deletion_result = request.app.database["events"].delete_one({"_id": id})
    if deletion_result.deleted_count:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"The event with id {id} was not found!")
