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

