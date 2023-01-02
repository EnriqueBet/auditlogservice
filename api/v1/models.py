from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(alias="_id")
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = False


class RegisteredUser(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class LogEvent(BaseModel):
    id: str = Field(alias="_id")
    name: str
    event_type: str
    detail: str
    user_id: str | None = None
    timestamp: datetime | None = None
    event_data: Dict[str, Any] | None = None
