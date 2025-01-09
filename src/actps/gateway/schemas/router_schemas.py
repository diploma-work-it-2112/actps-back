from datetime import datetime
from pydantic import BaseModel


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
