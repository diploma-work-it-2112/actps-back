from src.actps.domain.warning.model import Warning


def warning_to_dict(model: Warning):
    return {
        "id": model.id,
        "hostname": model.hostname,
        "type": model.type,
        "message": model.message,
        "created_at": model.created_at
    }

def dict_to_warning(data):
    return Warning(
        hostname=data["hostname"],
        type=data["type"],
        message=data["message"],
        created_at=data.get("created_at"),
        id=data.get("id")
    )

