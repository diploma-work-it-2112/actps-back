import uvicorn

from multiprocessing import Process
from queue import Queue
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.actps.gateway.urls import (
    get_router_router,
    get_pc_router,
    get_deamon_connection_router,
    get_logs_router,
)
from src.actps.config import FRONT_URL
from src.actps.trafic_monitor.json_parser import ScapyJSONTraficParse
from src.actps.trafic_monitor.monitor import TraficMonitor
from src.actps.trafic_monitor.trafic_storage_manager import TraficStorageManager
from src.actps.gateway.handler.trafic_monitoring_handler import redis_trafic_monitor_session


app = FastAPI(
    title="Adaptive Cyber Threat Protection System",
)

origins = [
    FRONT_URL,
    "http://localhost:5173",
    "http://localhost",
    "http://127.0.0.1:5173",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(get_router_router())
app.include_router(get_pc_router())
app.include_router(get_deamon_connection_router())
app.include_router(get_logs_router())

def start_uvicorn():
    uvicorn.run(app, host="0.0.0.0", port=8000)

trafic_logs_paht = "src/actps/trafic_monitor/logs/"

trafic_storage_manager = TraficStorageManager(trafic_logs_paht)

parser = ScapyJSONTraficParse()

trafic_monitor = TraficMonitor(
    log_writer=trafic_storage_manager,
    log_parser=parser,
    cache_service=redis_trafic_monitor_session,
    stream_key="trafic_logs_key"
)

if __name__ == "__main__":
    trafic_process = Process(target=trafic_monitor.run)
    server_process = Process(target=start_uvicorn)

    trafic_process.start()
    server_process.start()

    trafic_process.join()
    server_process.join()

    print("Main process finish")


