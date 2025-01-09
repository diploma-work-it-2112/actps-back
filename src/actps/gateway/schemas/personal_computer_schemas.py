from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class PCRequest(BaseModel):
    ip_address: str
    hostname: str
    router_id: Optional[int] = None


class PCResponse(BaseModel):
    id: int
    ip_address: str
    hostname: str
    router_id: Optional[int] = None
    created_at: datetime
