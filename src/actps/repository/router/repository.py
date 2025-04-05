from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete, update

from src.actps.core.repository import AbstractRepository
from src.actps.domain.router.model import Router
from .converter import router_to_dict, dict_to_router
from .statements import insert_router, select_router_by_id, update_router, delete_router, select_router, select_router_by_ip, get_last_router


class RouterRepository(AbstractRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, model: Router) -> Router:
        data = router_to_dict(model)
        
        id = await self.session.execute(
            insert_router,
            data
        )

        model._id = id.scalars().first()

        return model
    
    async def get(self, id: int) -> Router:
        res = await self.session.execute(
            select_router_by_id,
            {"id": id}
        )
        print(res)
        
        router = dict_to_router(res.one())

        return router

    async def get_by_ip(self, ip: str) -> Router:
        res = await self.session.execute(
            select_router_by_ip,
            {"ip": ip}
        )

        router = dict_to_router(res.one())
        print(router)

        return router

    async def get_list(self) -> list[Router]:
        res = await self.session.execute(
            select_router
        )
        print(res)
        res = res.all()

        return [dict_to_router(r) for r in res]

    async def get_last_router(self) -> Router:
        res = await self.session.execute(
            get_last_router 
        )
        res = res.one() 
        router = dict_to_router(res)
        return router

    async def update(self, model: Router):
        data = router_to_dict(model)
        
        await self.session.execute(
            update_router,
            data
        )

        return model


    async def delete(self, id: int):
        await self.session.execute(
            delete_router,
            {
                "id": id
            }
        )

