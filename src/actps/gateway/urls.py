from os import walk
from fastapi import APIRouter

from src.actps.gateway.handler import (
    connect_router_handler,
    get_all_routers_handler,

    connect_pc_handler,
    get_all_pc_handler,

    frontend_process_handler,
    frontend_system_load_handler,
)


def get_router_router() -> APIRouter:
    router = APIRouter(tags=["Router"], prefix="/v1")
    router.post("/router", status_code=200)(connect_router_handler)
    router.get("/router", status_code=200)(get_all_routers_handler)
    return router


def get_pc_router() -> APIRouter:
    router = APIRouter(tags=["PC"], prefix="/v1")
    router.post("/pc", status_code=200)(connect_pc_handler)
    router.get("/pc", status_code=200)(get_all_pc_handler)
    return router


def get_deamon_connection_router() -> APIRouter:
    router = APIRouter(tags=["Deamon Connection"], prefix="/v1")
    router.websocket("/ws/process")(frontend_process_handler)
    router.websocket("/ws/system_load")(frontend_system_load_handler)
    return router
