from sqlalchemy.ext.asyncio import AsyncSession

from src.actps.repository.personal_computer.repository import PCRepository
from src.actps.domain.pc.personal_computer import PC
from src.actps.repository.router.repository import RouterRepository
from src.actps.domain.router.model import Router


class RepositoryFactory:

    def __init__(self, session_factory: AsyncSession):
        self.session_factory = session_factory

    def get_repository(self, obj_type):
        if obj_type == Router:
            return RouterRepository(self.session_factory)
        elif obj_type == PC:
            return PCRepository(self.session_factory)
