from src.actps.core.unit_of_work import UnitOfWork
from src.actps.gateway.schemas.warning_schemas import WarningRequest
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.service.warning.warning_service import WarningService
from src.actps.views.warning_views import WarningViews


service = WarningService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def save_warning_handler(data: WarningRequest):
    await service.create_warning(
        data=data,
        uow=uow
    )
    return ["200"]


async def get_all_warning():
    warnings = await WarningViews.get_all_warnings_view(engine=init_engine())
    return warnings


async def get_latests_warning():
    warning = await WarningViews.get_latest_warning_view(engine=init_engine())
    return warning
