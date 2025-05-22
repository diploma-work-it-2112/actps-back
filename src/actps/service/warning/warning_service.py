

from pydantic import BaseModel

from src.actps.core.unit_of_work import UnitOfWork
from src.actps.domain.warning.model import Warning


class WarningService:

    async def create_warning(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ):
        warning = Warning(
            hostname=data.hostname,
            type=data.type,
            message=data.message,
        )

        async with uow as uow:
            await uow.add(warning)
            await uow.commit()

