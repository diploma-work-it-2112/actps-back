from datetime import datetime

from src.actps.domain.logs import PackageLog, ProcessLog


def package_log_to_dict(model: PackageLog):
    model_dict = {
        "id": model.id,
        "message": model.message,
        "pc_id": model.pc_id,
        "web_host_name": model.web_host_name,
        "ip_source": model.ip_source,
        "ip_destination": model.ip_destination,
        "mac_source": model.mac_source,
        "mac_destination": model.mac_destination,
        "port_source": model.port_source,
        "port_destination": model.port_destination,
        "time": model.time,
        "created_at": model.created_at
    }
    return model_dict


def dict_to_package_log(pl):
    return PackageLog(
        ip_source=pl["ip_source"],
        ip_destination=pl["ip_destination"],
        mac_source=pl["mac_source"],
        mac_destination=pl["mac_destination"],
        port_destinatin=pl["port_destination"],
        time=pl["time"],
        web_host_name=pl.get("web_host_name"),
        pc_id=pl.get("pc_id"),
        message=pl.get("message"),
        id=pl.get("id"),
        created_at=pl.get("created_at")
    )

def process_log_to_dict(model: ProcessLog):
    return {
        "id": model.id,
        "name": model.name,
        "path": model.path,
        "pred": model.pred,
        "created_at": model.created_at
    }

def dict_to_process_log(pl):
    return ProcessLog(
        name=pl["name"],
        path=pl["path"],
        pred=pl["pred"],
        created_at=pl.get("created_at"),
        id=pl.get("id")
    )

