from datetime import datetime

from src.actps.domain.pc import PC


def pc_to_dict(model: PC):
    model_dict = {
        "id": model.id,
        "ip_address": model.ip_address,
        "hostname": model.hostname,
        "router_id": model.router_id,
        "created_at": model.created_at
    }

    return model_dict


def dict_to_pc(pc):
    return PC(
        id=pc.id,
        ip_address=pc.ip_address,
        hostname=pc.hostname,
        router_id=pc.router_id,
        created_at=pc.created_at
    )

