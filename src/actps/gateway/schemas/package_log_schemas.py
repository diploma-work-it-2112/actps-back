from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PackageLogRequest(BaseModel):
    ip_source: str
    ip_destination: str
    mac_source: str
    mac_destination: str
    port_source: str
    port_destination: str
    time: datetime
    web_host_name: Optional[str] = None
    pc_host_name: Optional[str] = None
    message: Optional[str] = None


class PackageLogResponse(BaseModel):
    id: int
    message: Optional[str] = None
    ip_source: str
    ip_destination: str
    mac_source: str
    mac_destination: str
    port_source: str
    port_destination: str
    web_host_name: Optional[str] = None
    pc_id: Optional[int] = None
    time: datetime
    created_at: datetime

