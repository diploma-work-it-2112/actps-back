from fastapi import Request

from src.actps.gateway.schemas.personal_computer_schemas import PCRequest, PCHeartbeatRequest
from src.actps.integrations.redis.redis import RedisCacheService
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.core.unit_of_work import UnitOfWork
from src.actps.service.personal_computer import PCService
from src.actps.views import PCViews
from src.actps.gateway.schemas import AllWorkingHostsResponse


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


async def pc_heartbeat_handler(request: Request, data: PCHeartbeatRequest):
    await service.heartbeat_pc_service(
        data=data,
        uow=uow,
        pc_ip=request.client.host,
        cache_service=redis_service
    )
    return 200


async def get_all_working_hosts():
    keys = redis_service.get_all_keys()
    res = {}

    for key in keys:
        value = redis_service.get(key)
        res[key] = value
    
    response = AllWorkingHostsResponse(result=res)
    return response
