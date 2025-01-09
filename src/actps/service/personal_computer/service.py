from pydantic import BaseModel

from src.actps.core.unit_of_work import UnitOfWork 
from src.actps.domain.pc import PC


class PCService:

    async def connect_pc(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ) -> PC:
        
        pc = PC(
            ip_address=data.ip_address,
            hostname=data.hostname,
            router_id=data.router_id
        )

        async with uow as uow:
            pc = await uow.add(pc)
            await uow.commit()

        return pc
