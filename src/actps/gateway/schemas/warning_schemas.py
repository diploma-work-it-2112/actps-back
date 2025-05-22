from pydantic import BaseModel
from datetime import datetime


class WarningRequest(BaseModel):
    hostname: str 
    type: str 
    message: str

class WarningResponse(BaseModel):
    id: int 
    hostname: str 
    type: str 
    message: str 
    created_at: datetime
