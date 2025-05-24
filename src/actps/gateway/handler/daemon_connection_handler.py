import uuid
import asyncio
import aiohttp

from fastapi import WebSocket, WebSocketDisconnect


connections = {
    "process": {},
    "system_load": {}
}

async def connect_to_app(endpoint, conn_id, endpoint_ip):
    url = f"http://{endpoint_ip}:8080/ws/{endpoint}"
    endpoint = endpoint.split("?")[0]
    try:
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(url) as ws:
                async for message in ws:
                    data = message.data
                    if conn_id in connections[endpoint]:
                        connection = connections[endpoint][conn_id]
                        if not connection.client_state.name == "CLOSED":
                            await connection.send_text(data)
    except Exception as e:
        print(e)
                


async def frontend_process_handler(ws: WebSocket, ip_address: str):
    await ws.accept()
    connection_id = str(uuid.uuid4())
    connections["process"][connection_id] = ws
    task = asyncio.create_task(connect_to_app(f"process?sort_by=name", connection_id, ip_address))
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        connections["process"].pop(connection_id, None)
        task.cancel()

async def frontend_system_load_handler(ws: WebSocket, ip_address: str):
    await ws.accept()
    connection_id = str(uuid.uuid4())
    connections["system_load"][connection_id] = ws
    task = asyncio.create_task(connect_to_app(f"system_load", connection_id, ip_address))
    try:
        while True:
            await ws.receive_text()
    except WebSocketDisconnect:
        connections["system_load"].pop(connection_id, None)
        task.cancel()


async def get_folder_tree_handler(ip_address: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://{ip_address}:8080/folder-tree") as resp:
            tree = await resp.json()
    
    return tree

