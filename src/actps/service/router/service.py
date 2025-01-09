from pydantic import BaseModel

from src.actps.core.unit_of_work import UnitOfWork
from src.actps.domain.router.model import Router


class RouterService:

    async def connect_router(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ) -> Router:
        
        router = Router(
            model_name=data.model_name,
            ip_address=data.ip_address,
            hostname=data.hostname
        )

        async with uow as uow:
            router = await uow.add(router)
            await uow.commit()

        return router
