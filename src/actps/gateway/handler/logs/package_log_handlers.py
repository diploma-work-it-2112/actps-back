from src.actps.gateway.schemas import PackageLogRequest, PackageLogResponse
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.core.unit_of_work import UnitOfWork
from src.actps.service.logs import PackageLogService
from src.actps.views.logs import PackageLogViews


service = PackageLogService() 
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def receive_package_log_from_pc_handler(data: PackageLogRequest):
    await service.create_package_log_from_pc(
        data=data,
        uow=uow
    )

    return 200


async def get_all_packages_logs_from_pc_by_hostname_handler(hostname: str):
    logs = await PackageLogViews.get_package_log_by_pc_hostname_view(pc_hostname=hostname, engine=init_engine())

    return logs
