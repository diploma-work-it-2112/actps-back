from fastapi import File, UploadFile

from src.actps.core.unit_of_work import UnitOfWork
from src.actps.gateway.schemas import ProcessLogRequest
from src.actps.integrations.postgres.engine import get_session
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.service.logs.process_log_service import ProcessLogService


service = ProcessLogService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def save_process_log_handler(data: ProcessLogRequest):
    await service.create_process_log(
        data=data,
        uow=uow
    ) 
    return ["200"]
