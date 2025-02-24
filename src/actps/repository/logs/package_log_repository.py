from sqlalchemy.ext.asyncio import AsyncSession

from src.actps.core.repository import AbstractRepository
from src.actps.domain.logs import PackageLog
from .converter import package_log_to_dict, dict_to_package_log
from .statements import insert_package_log, select_package_log, select_package_log_by_id, select_package_log_by_pc_id, update_package_log, delete_package_log


class PackageLogRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: PackageLog) -> PackageLog:
        data = package_log_to_dict(model)
        
        result = await self.session.execute(
            insert_package_log,
            data
        )
        
        model._id = result.scalars().first()
        return model

    async def get(self, id: int) -> PackageLog:
        result = await self.session.execute(
            select_package_log_by_id,
            {"id": id}
        )
        
        package_log = dict_to_package_log(result.one())
        return package_log

    async def get_list(self) -> list[PackageLog]:
        result = await self.session.execute(
            select_package_log
        )
        records = result.all()

        return [dict_to_package_log(record) for record in records]

    async def update(self, model: PackageLog) -> PackageLog:
        data = package_log_to_dict(model)
        
        await self.session.execute(
            update_package_log,
            data
        )
        return model

    async def delete(self, id: int):
        await self.session.execute(
            delete_package_log,
            {"id": id}
        )

    async def get_by_pc_id(self, pc_id: int) -> list[PackageLog]:
        result = await self.session.execute(
            select_package_log_by_pc_id,
            {"pc_id": pc_id}
        )
        records = result.all()

        return [dict_to_package_log(record) for record in records]

