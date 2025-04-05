from datetime import datetime

from src.actps.domain.pc.personal_computer import PC
from src.actps.domain.router.model import Router


def router_to_dict(model: Router):
    model_dict = {
        "id": model.id,
        "model_name": model.model_name,
        "ip_address": model.ip_address,
        "hostname": model.hostname,
        "created_at": model.created_at,
        "color": model.color
    }

    return model_dict


def dict_to_router(router):
    return Router(
        id=router.router_id,
        model_name=router.model_name,
        ip_address=router.router_id,
        hostname=router.router_hostname,
        created_at=router.router_created_at,
        computers=[
            PC(
                id=computer['computer_id'],
                ip_address=computer['computer_ip'],
                hostname=computer['computer_hostname'],
                router_id=router.router_id,
                created_at=computer['computer_created_at']
            ) for computer in router.computers
        ] if router.computers is not None else [],
        color=router.router_color
    )
