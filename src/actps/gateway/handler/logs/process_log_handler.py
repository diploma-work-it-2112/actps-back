from fastapi import File, UploadFile
import json

from src.actps.core.unit_of_work import UnitOfWork
from src.actps.gateway.schemas import ProcessLogRequest
from src.actps.integrations.postgres.engine import get_session, init_engine
from src.actps.repository.repository_factory import RepositoryFactory
from src.actps.service.logs.process_log_service import ProcessLogService
from src.actps.views.logs.process_logs_views import ProcessLogViews


service = ProcessLogService()
uow = UnitOfWork(session_factory=get_session, repository_factory=RepositoryFactory)


async def save_process_log_handler(data: ProcessLogRequest):
    await service.create_process_log(
        data=data,
        uow=uow
    ) 
    return ["200"]


async def get_process_log_infor_handler(name):
    log = await ProcessLogViews.get_process_log_by_name_view(
        name=name,
        engine=init_engine()
    )
    return log

