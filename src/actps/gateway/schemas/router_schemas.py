from datetime import datetime
from typing import List
from pydantic import BaseModel

from .personal_computer_schemas import PCResponse


class RouterRequest(BaseModel):
    model_name: str 
    ip_address: str
    hostname: str


class RouterResponse(BaseModel):
    id: int
    model_name: str
    ip_address: str
    hostname: str
    created_at: datetime
    computers: List[PCResponse]
    color: str
