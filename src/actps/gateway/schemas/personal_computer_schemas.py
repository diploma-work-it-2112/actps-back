from datetime import datetime
from pydantic import BaseModel
from typing import Dict, Optional


class PCRequest(BaseModel):
    hostname: str
    router_ip: str


class PCResponse(BaseModel):
    id: int
    ip_address: str
    hostname: str
    router_id: Optional[int] = None
    created_at: datetime


class PCHeartbeatRequest(BaseModel):
    hostname: str
    open_ports: Dict


class AllWorkingHostsResponse(BaseModel):
    result: Dict
