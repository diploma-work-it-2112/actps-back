from datetime import datetime

from src.actps.core.base_entity import AbstractBaseEntity


class ProcessLog(AbstractBaseEntity):
    def __init__(
        self,
        name: str,
        path: str,
        pred: str,
        created_at: datetime = None,
        id: int = None
    ):
        self._id = id
        self._name = name
        self._path = path
        self._pred = pred
        self._created_at = created_at or datetime.utcnow()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> str:
        return self._path

    @property
    def pred(self) -> str:
        return self._pred

    @property
    def created_at(self) -> datetime:
        return self._created_at
