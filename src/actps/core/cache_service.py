from abc import ABC, abstractmethod
from typing import Optional


class AbstractCacheService(ABC):
    
    @abstractmethod
    def set(self, key, value, expiration: Optional[int] = None):
        raise NotImplementedError

    @abstractmethod 
    def hset(self, key, value, expiration: Optional[int] = None):
        raise NotImplementedError
    
    @abstractmethod
    def get(self, key: str) -> Optional[str]:
        raise NotImplementedError

    @abstractmethod
    def exists(self, key: str) -> bool:
        return NotImplementedError

