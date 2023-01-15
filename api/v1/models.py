from pydantic import BaseModel, Field
from datetime import datetime
from typing import Dict, Any
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    full_name: str | None = None
    disabled: bool | None = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class RegisteredUser(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class LogEvent(BaseModel):
    name: str
    event_type: str
    detail: str
    user_id: PyObjectId | None = Field(default_factory=PyObjectId)
    timestamp: datetime | None = None
    event_data: Dict[str, Any] | None = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class StoredLogEvent(LogEvent):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    