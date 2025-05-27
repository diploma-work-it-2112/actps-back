from pydantic import BaseModel
from sqlalchemy.orm.exc import NoResultFound

from src.actps.core.cache_service import AbstractCacheService
from src.actps.core.unit_of_work import UnitOfWork 
from src.actps.domain.pc import PC
from src.actps.domain.router import Router


class PCService:

    async def connect_pc(
        self,
        data: BaseModel,
        uow: UnitOfWork,
        pc_ip: str,
        cache_service: AbstractCacheService
    ) -> PC:

        async with uow as uow:
            try:
                router_repo = await uow.get_repository(Router)
                router = await router_repo.get_by_ip(data.router_ip)
            except NoResultFound as e:
                router_repo = await uow.get_repository(Router)
                list_router = await router_repo.get_list()
                if len(list_router) != 0:
                    color_index = list_router[-1].id 
                else:
                    color_index = 1
                router = Router(
                    model_name="router name",
                    ip_address=data.router_ip,
                    hostname=f"router {data.router_ip}",
                    color_index=color_index
                )
                router = await uow.add(router)

            pc = PC(
                ip_address=pc_ip,
                hostname=data.hostname,
                router_id=router.id
            )
            pc = await uow.add(pc)
            
            cache_service.set(pc.hostname, pc.ip_address, 40)

            await uow.commit()


        return pc


    async def heartbeat_pc_service(
        self,
        data: BaseModel,
        uow: UnitOfWork,
        pc_ip: str,
        cache_service: AbstractCacheService
    ):
        
        async with uow as uow:
            pc_ip_from_cache = cache_service.get(data.hostname)
            if pc_ip_from_cache != pc_ip:
                pc_repo = await uow.get_repository(PC)
                pc = await pc_repo.get_by_hostname(data.hostname)
                pc.update_ip(pc_ip)
                await uow.update(pc)

            await uow.commit()

        cache_service.set(data.hostname, pc_ip, 40)

        data_to_save_cache = data.open_ports
        data_to_save_cache.update({"hostname": data.hostname})

        cache_service.hset(pc_ip, data_to_save_cache)

