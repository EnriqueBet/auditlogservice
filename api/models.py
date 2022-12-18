from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class LogEvent(BaseModel):
    name: str
    source: str
    description: str
    timestamp: datetime
    event_type: str
    data: Optional[Dict[str, Any]]

class LogEventRead(LogEvent):
    id: int
