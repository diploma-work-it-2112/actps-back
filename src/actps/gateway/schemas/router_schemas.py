from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

from .personal_computer_schemas import PCResponse


class RouterRequest(BaseModel):
    model_name: str 
    ip_address: str
    hostname: str
    group_name: Optional[str] = None


class RouterResponse(BaseModel):
    id: int
    model_name: str
    ip_address: str
    hostname: str
    created_at: datetime
    computers: List[PCResponse]
    color: str
    group_name: Optional[str] = None
