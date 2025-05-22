from sqlalchemy.ext.asyncio import AsyncSession

from src.actps.core.repository import AbstractRepository
from src.actps.domain.logs import ProcessLog
from .converter import process_log_to_dict, dict_to_process_log 
from .statements import insert_process_log, select_process_log, select_process_log_by_id, update_process_log, delete_process_log


class ProcessLogRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: ProcessLog) -> ProcessLog:
        data = process_log_to_dict(model)

        result = await self.session.execute(
            insert_process_log,
            data
        )

        model._id = result.scalars().first()
        return model

    async def get(self, id: int) -> ProcessLog:
        result = await self.session.execute(
            select_process_log_by_id,
            {"id": id}
        )

        process_log = dict_to_process_log(result.one())
        return process_log

    async def get_list(self) -> list[ProcessLog]:
        result = await self.session.execute(
            select_process_log
        )
        records = result.all()

        return [dict_to_process_log(record) for record in records]

    async def update(self, model: ProcessLog) -> ProcessLog:
        data = process_log_to_dict(model)

        await self.session.execute(
            update_process_log,
            data
        )
        return model

    async def delete(self, id: int):
        await self.session.execute(
            delete_process_log,
            {"id": id}
        )

