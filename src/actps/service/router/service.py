from pydantic import BaseModel

from src.actps.core.unit_of_work import UnitOfWork
from src.actps.domain.router.model import Router


class RouterService:

    async def connect_router(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ) -> Router:
        
        async with uow as uow:

            router_repo = await uow.get_repository(Router)
            list_router = await router_repo.get_list()
            if len(list_router) != 0:
                color_index = list_router[-1].id 
            else:
                color_index = 1
            router = Router(
                model_name=data.model_name,
                ip_address=data.ip_address,
                hostname=data.hostname,
                group_name=data.group_name,
                color_index=color_index
            )

            router = await uow.add(router)
            await uow.commit()

        return router


    async def update_router(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ):
        async with uow as uow:
            router = await uow.get(data.id, Router)
            if router.hostname != data.hostname:
                raise ValueError("Wrong hostname and id")
            router.update(
                ip_address=data.ip_address,
                new_model_name=data.new_model_name,
                new_color=data.new_color,
                new_group_name=data.new_group_name
            )
            await uow.update(router)

            await uow.commit()

