from datetime import datetime

from src.actps.domain.router.model import Router


def router_to_dict(model: Router):
    model_dict = {
        "id": model.id,
        "model_name": model.model_name,
        "ip_address": model.ip_address,
        "hostname": model.hostname,
        "created_at": model.created_at
    }

    return model_dict


def dict_to_router(router):
    return Router(
        id=router.id,
        model_name=router.model_name,
        ip_address=router.ip_address,
        hostname=router.hostname,
        created_at=router.created_at
    )

