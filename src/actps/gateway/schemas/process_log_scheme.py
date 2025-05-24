from datetime import datetime
from typing import Dict
from pydantic import BaseModel


class ProcessLogRequest(BaseModel):
    name: str 
    pred: str
    report: Dict


class ProcessLogResponse(BaseModel):
    id: int 
    name: str 
    path: str 
    pred: str
    report: Dict
    created_at: datetime
