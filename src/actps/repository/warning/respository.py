from sqlalchemy.ext.asyncio import AsyncSession

from src.actps.core.repository import AbstractRepository
from src.actps.domain.warning.model import Warning
from .converter import warning_to_dict, dict_to_warning
from .statements import (
    insert_warning,
    select_warning,
    select_warning_by_id,
    update_warning,
    delete_warning
)

class WarningRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Warning) -> Warning:
        data = warning_to_dict(model)

        result = await self.session.execute(
            insert_warning,
            data
        )

        model._id = result.scalars().first()
        return model

    async def get(self, id: int) -> Warning:
        result = await self.session.execute(
            select_warning_by_id,
            {"id": id}
        )

        warning = dict_to_warning(result.one())
        return warning

    async def get_list(self) -> list[Warning]:
        result = await self.session.execute(
            select_warning
        )
        records = result.all()

        return [dict_to_warning(record) for record in records]

    async def update(self, model: Warning) -> Warning:
        data = warning_to_dict(model)

        await self.session.execute(
            update_warning,
            data
        )
        return model

    async def delete(self, id: int):
        await self.session.execute(
            delete_warning,
            {"id": id}
        )

