import redis

from typing import List, Optional

from src.actps.core.cache_service import AbstractCacheService
from src.actps.config import REDIS_URL, REDIS_PORT, REDIS_PASSWORD


class RedisCacheService(AbstractCacheService):

    def __init__(
            self, 
            host: str = REDIS_URL, 
            port: int = REDIS_PORT, 
            db: int = 1, 
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

    def get_all_keys(self) -> List:
        cursor = 0
        keys = []
        while True:
            cursor, keys = self._client.scan(cursor, count=50)
            keys.extend(keys)
            if cursor == 0:
                break
        return keys


    def xadd(self, strema_key, data):
        try:
            self._client.xadd(strema_key, data, id="*")
        except:
            pass


    def xread(self, stream_key, min, max, count):
        self._client.xrange(stream_key, min=min, max=max, count=count)


    def xtrim(self, stream_key, maxlen):
        self._client.xtrim(stream_key, maxlen=maxlen)

    def xdel(self, stream_key, ids):
        self._client.xdel(stream_key, *ids)

    def xlen(self, stream_key):
        return self._client.xlen(stream_key)
