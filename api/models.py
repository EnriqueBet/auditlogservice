import uuid

from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class LogEvent(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    event_type: str
    description: str
    source: Optional[str] = None
    timestamp: Optional[datetime] = None

    # class Config:
    #     allow_population_by_field_name = True
    #     schema_extra = {
    #         "example": {
    #             "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
    #             "name": "Some Event Name",
    #             "description": "Some Event Description",
    #             "event_type": "Some Event Type"
    #         }
    #     }
    
class LogEventRead(LogEvent):
    id: int
