import uuid

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class RegisteredUser(User):
    hashed_password: str


class LogEvent(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    event_type: str
    detail: str
    user: User | None = None
    timestamp: datetime | None = None
    event_data: Dict[str: Any] | None = None
