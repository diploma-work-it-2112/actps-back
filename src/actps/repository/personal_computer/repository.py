from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.actps.core.repository import AbstractRepository
from src.actps.domain.pc import PC
from .converter import pc_to_dict, dict_to_pc
from .statements import insert_pc, select_pc_by_id, update_pc, delete_pc, select_pc, select_pc_by_hostname


class PCRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: PC) -> PC:
        data = pc_to_dict(model)
        
        id = await self.session.execute(
            insert_pc,
            data
        )

        model._id = id.scalars().first()

        return model
    
    async def get(self, id: int) -> PC:
        res = await self.session.execute(
            select_pc_by_id,
            {"id": id}
        )
        
        pc = dict_to_pc(res.one())

        return pc

    async def get_by_hostname(self, hostname: str) -> PC:
        res = await self.session.execute(
            select_pc_by_hostname,
            {"hostname": hostname}
        )

        pc = dict_to_pc(res.one())
        return pc

    async def get_list(self) -> list[PC]:
        res = await self.session.execute(
            select_pc
        )
        res = res.all()

        return [dict_to_pc(r) for r in res]

    async def update(self, model: PC):
        data = pc_to_dict(model)
        
        await self.session.execute(
            update_pc,
            data
        )

        return model


    async def delete(self, id: int):
        await self.session.execute(
            delete_pc,
            {
                "id": id
            }
        )

