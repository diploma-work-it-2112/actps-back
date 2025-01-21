import uuid

from fastapi import WebSocket, WebSocketDisconnect


connections = {
}

async def connect_to_app(endpoint, conn_id):
    url = f"http://127.0.0.1:8080/ws/{endpoint}"
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            async for message in ws:
                data = message.data
                connection = connections[conn_id]
                await connection.send_text(data)
                


async def frontend_process_handler(ws: WebSocket, sort: str):
    await ws.accept()
    connection_id = str(uuid.uuid4())
    connections[connection_id] = ws

    task = asyncio.create_task(connect_to_app(f"process?sort_by={sort}", connection_id))
    try:
        while True:
            await ws.receive_text()  
    except WebSocketDisconnect:
        connections.pop(connection_id)
        task.cancel()

