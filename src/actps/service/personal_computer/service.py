from pydantic import BaseModel

from src.actps.core.unit_of_work import UnitOfWork 
from src.actps.domain.pc import PC
from src.actps.domain.router import Router


class PCService:

    async def connect_pc(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ) -> PC:

        async with uow as uow:
            try:
                router_repo = await uow.get_repository(Router)
                router = await router_repo.get_by_ip(data.router_ip)
                print(router)
            except Exception as e:
                print(e)
                # router = Router(
                #     model_name="router name",
                #     ip_address=data.router_ip,
                #     hostname=f"router {data.router_ip}"
                # )
                # router = await uow.add(router)

            pc = PC(
                ip_address=data.ip_address,
                hostname=data.hostname,
                router_id=router.id
            )
            pc = await uow.add(pc)
            await uow.commit()

        return pc
