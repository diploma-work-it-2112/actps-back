import json

from fastapi import WebSocket, WebSocketDisconnect

from src.actps.integrations.redis.redis import RedisCacheService


redis_trafic_monitor_session = RedisCacheService(db=2)


async def monitor_trafic_handler(ws: WebSocket):
    await ws.accept()
    try:
        first_id = None
        while True: 
            data = redis_trafic_monitor_session.xrange(stream_key="trafic_logs_key", min="-", max="+", count=50)
            count = 0
            json_data = json.dumps(data)
            for id, fields in data:
                if count == 0 and first_id == id:
                    break
                elif count == 0:
                    first_id = id
                json_data = json.dumps(fields)
                await ws.send_text(json_data)
    except: 
        pass

