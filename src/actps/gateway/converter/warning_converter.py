from sqlalchemy import Row
from typing import List

from src.actps.domain.warning.model import Warning
from src.actps.gateway.schemas.warning_schemas import WarningResponse


class WarningConverter:

    @classmethod
    def row_to_warning(cls, row: Row) -> WarningResponse:
        return WarningResponse(
            id=row.id,
            hostname=row.hostname,
            type=row.type,
            message=row.message,
            created_at=row.created_at
        )

    @classmethod
    def row_to_warning_list(cls, rows) -> List[WarningResponse]:
        return [cls.row_to_warning(row) for row in rows]

    @classmethod
    def model_to_warning(cls, warning: Warning) -> WarningResponse:
        return WarningResponse(
            id=warning.id,
            hostname=warning.hostname,
            type=warning.type,
            message=warning.message,
            created_at=warning.created_at
        )

    @classmethod
    def model_to_warning_list(cls, warnings: List[Warning]) -> List[WarningResponse]:
        return [cls.model_to_warning(w) for w in warnings]

