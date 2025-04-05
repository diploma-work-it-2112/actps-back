from fastapi import Request

from src.actps.gateway.schemas.personal_computer_schemas import PCRequest
from src.actps.integrations.redis.redis import RedisCacheService
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.core.unit_of_work import UnitOfWork
from src.actps.service.personal_computer import PCService
from src.actps.views import PCViews


service = PCService()
redis_service = RedisCacheService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def connect_pc_handler(request: Request, data: PCRequest):
    pc_ip = request.client.host
    await service.connect_pc(
        data=data,
        uow=uow,
        pc_ip=pc_ip,
        cache_service=redis_service,
    )

    return 200


async def get_all_pc_handler():
    psc = await PCViews.get_all_pcs_view(engine=init_engine())

    return psc
