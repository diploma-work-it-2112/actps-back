from abc import ABC, abstractmethod
from .base_entity import AbstractBaseEntity


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, model: AbstractBaseEntity):
        raise NotImplementedError
    
    @abstractmethod
    async def get(self, id) -> AbstractBaseEntity:
        raise NotImplementedError
    
    @abstractmethod
    async def get_list(self) -> list[AbstractBaseEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update(self, model: AbstractBaseEntity):
        raise NotImplementedError
    
    @abstractmethod
    async def delete(self, id):
        raise NotImplementedError
