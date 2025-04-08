from fastapi import WebSocket, WebSocketDisconnect

from src.actps.integrations.redis.redis import RedisCacheService


redis_trafic_monitor_session = RedisCacheService(db=2)


async def monitor_trafic_handler(ws: WebSocket):
    pass

