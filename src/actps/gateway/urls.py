from os import walk
from fastapi import APIRouter

from src.actps.gateway.handler import (
    connect_router_handler,
    get_all_routers_handler,
    update_router_handler,

    connect_pc_handler,
    get_all_pc_handler,
    pc_heartbeat_handler,
    get_all_working_hosts,

    frontend_process_handler,
    frontend_system_load_handler,

    monitor_trafic_handler,

    save_warning_handler
)
from src.actps.gateway.handler.logs import (
    receive_package_log_from_pc_handler,
    get_all_packages_logs_from_pc_by_hostname_handler,

    save_process_log_handler,
)


def get_router_router() -> APIRouter:
    router = APIRouter(tags=["Router"], prefix="/v1")
    router.post("/router", status_code=200)(connect_router_handler)
    router.get("/router", status_code=200)(get_all_routers_handler)
    router.patch("/router", status_code=200)(update_router_handler)
    return router


def get_pc_router() -> APIRouter:
    router = APIRouter(tags=["PC"], prefix="/v1")
    router.post("/pc", status_code=200)(connect_pc_handler)
    router.get("/pc", status_code=200)(get_all_pc_handler)
    router.post("/pc/heartbeat", status_code=200)(pc_heartbeat_handler)
    router.get("/pc/heartbeat", status_code=200)(get_all_working_hosts)
    return router


def get_deamon_connection_router() -> APIRouter:
    router = APIRouter(tags=["Deamon Connection"], prefix="/v1")
    router.websocket("/ws/process/{ip_address}")(frontend_process_handler)
    router.websocket("/ws/system_load/{ip_address}")(frontend_system_load_handler)
    return router


def get_logs_router() -> APIRouter:
    router = APIRouter(tags=["Logs"], prefix="/v1")
    router.post("/log/package", status_code=200)(receive_package_log_from_pc_handler)
    router.get("/log/package/{hostname}", status_code=200)(get_all_packages_logs_from_pc_by_hostname_handler)

    router.post("/log/process", status_code=200)(save_process_log_handler)
    return router


def get_trafic_router() -> APIRouter:
    router = APIRouter(tags=["Trafic"], prefix="/v1")
    router.websocket("/ws/trafic/")(monitor_trafic_handler)
    return router


def get_warning_router() -> APIRouter:
    router = APIRouter(tags=["Warning"], prefix="/v1")
    router.post("/warning", status_code=200)(save_warning_handler)
    return router
