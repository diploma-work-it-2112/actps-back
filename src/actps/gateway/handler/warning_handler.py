from src.actps.core.unit_of_work import UnitOfWork
from src.actps.gateway.schemas.warning_schemas import WarningRequest
from src.actps.integrations.postgres.engine import get_session
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.service.warning.warning_service import WarningService


service = WarningService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def save_warning_handler(data: WarningRequest):
    await service.create_warning(
        data=data,
        uow=uow
    )
    return ["200"]
