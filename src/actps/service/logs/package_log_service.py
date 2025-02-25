from pydantic import BaseModel 

from src.actps.core.unit_of_work import UnitOfWork 
from src.actps.domain.logs import PackageLog 
from src.actps.domain.pc import PC


class PackageLogService:

    async def create_package_log_from_pc(
        self,
        data: BaseModel,
        uow: UnitOfWork
    ) -> PackageLog:

        async with uow as uow:
            pc_repository = await uow.get_repository(PC)
            pc_id = await pc_repository.get_by_hostname(data.pc_hostname)
            package_log = PackageLog(
                ip_source=data.ip_source,
                ip_destination=data.ip_destination,
                mac_source=data.mac_source,
                mac_destination=data.mac_destination,
                port_source=data.port_source,
                port_destination=data.port_destination,  
                time=data.time,
                web_host_name=data.web_host_name,
                pc_id=pc_id,
                message=data.message,
                id=data.id,
                created_at=data.created_at
            )

            await uow.add(package_log)
            await uow.commit()

        return package_log
