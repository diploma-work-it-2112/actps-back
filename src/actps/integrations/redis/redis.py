import redis

from typing import Optional

from actps.core.cache_service import AbstractCacheService
from actps.config import REDIS_URL, REDIS_PORT, REDIS_PASSWORD


class RedisCacheService(AbstractCacheService):

    def __init__(
            self, 
            host: str = REDIS_URL, 
            port: int = REDIS_PORT, 
            db: int = 0, 
            password: Optional[str] = REDIS_PASSWORD
    ):
        self._client = redis.Redis(host=host, port=port, db=db, password=password)

    def set(self, key: str, value: str, expiration: Optional[int] = None) -> None:
        self._client.set(key, value, ex=expiration)

    def get(self, key: str) -> Optional[str]:
        value = self._client.get(key)
        return value.decode('utf-8') if value else None

    def exists(self, key: str) -> bool:
        return self._client.exists(key) > 0

