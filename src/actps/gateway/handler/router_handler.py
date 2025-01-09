from src.actps.core.unit_of_work import UnitOfWork
from src.actps.gateway.schemas.router_schemas import RouterRequest
from src.actps.repository import RepositoryFactory
from src.actps.service.router import RouterService
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.views import RouterViews


service = RouterService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def connect_router_handler(data: RouterRequest):
    await service.connect_router(
        data=data,
        uow=uow
    )

    return 200


async def get_all_routers_handler():
    routers = await RouterViews.get_all_routers_view(engine=init_engine())

    return routers
