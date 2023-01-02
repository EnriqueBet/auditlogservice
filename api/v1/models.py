import uuid

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4(), alias="_id")
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RegisteredUser(User):
    hashed_password: str


class LogEvent(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    user_id: str
    name: str
    event_type: str
    detail: str
    timestamp: datetime | None = None
    event_data: Dict[str, Any] | None = None
