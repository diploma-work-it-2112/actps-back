import json
from sqlalchemy import Row
from typing import List

from src.actps.domain.logs.process_log import ProcessLog
from src.actps.gateway.schemas.process_log_scheme import ProcessLogResponse


class ProcessLogConverter:

    @classmethod
    def row_to_process_log(cls, row: Row) -> ProcessLogResponse:

        with open(row.path, "r") as f:
            report = json.load(f)
        
        return ProcessLogResponse(
            id=row.id,
            name=row.name,
            path=row.path,
            pred=row.pred,
            report=report,
            created_at=row.created_at
        )

    @classmethod
    def row_to_process_log_list(cls, rows) -> List[ProcessLogResponse]:
        return [cls.row_to_process_log(row) for row in rows]

    @classmethod
    def model_to_process_log(cls, model: ProcessLog) -> ProcessLogResponse:
        with open(model.path, "r") as f:
            report = json.load(f)

        return ProcessLogResponse(
            id=model.id,
            name=model.name,
            path=model.path,
            pred=model.pred,
            report=report,
            created_at=model.created_at
        )

    @classmethod
    def model_to_process_log_list(cls, models: List[ProcessLog]) -> List[ProcessLogResponse]:
        return [cls.model_to_process_log(model) for model in models]

