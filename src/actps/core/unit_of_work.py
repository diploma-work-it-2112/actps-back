from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from src.actps.repository import RepositoryFactory
from .base_entity import AbstractBaseEntity


class AbstractUnitOfWork(ABC):

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    @abstractmethod
    async def commit(self):
        raise NotImplementedError
    
    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def get_repository(self, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def add(self, model: AbstractBaseEntity):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def get(self, id, obj_type):
        raise NotImplementedError

    @abstractmethod
    async def update(eslf, model: AbstractBaseEntity):
        raise NotImplementedError



class UnitOfWork(AbstractUnitOfWork):
    
    def __init__(self, session_factory: AsyncSession, repository_factory: RepositoryFactory):
        self.session_factory = session_factory
        self.repositories = {}
        self.repository_factory = repository_factory

    async def __aenter__(self):
        self.session = await self.session_factory()
        self.repository_factory = self.repository_factory(self.session)
        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__()
        await self.session.close()
        self.repositories = {}
        self.repository_factory = self.repository_factory.__class__

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def add(self, model: AbstractBaseEntity):
        repository = await self.get_repository(type(model))
        response = await repository.add(model)
        return response
    
    async def get_repository(self, obj_type):
        repo = self.repositories.get(obj_type)
        if repo is None:
            repo = self.repository_factory.get_repository(obj_type)
            print(obj_type)
            self.repositories[obj_type] = repo
        return repo

    async def delete(self, id, obj_type):
        repository = await self.get_repository(obj_type)
        await repository.delete(id)

    async def get(self, id, obj_type):
        repository = await self.get_repository(obj_type)
        response = await repository.get(id)
        return response

    async def update(self, model: AbstractBaseEntity):
        repository = await self.get_repository(type(model))
        response = await repository.update(model)
        return response


