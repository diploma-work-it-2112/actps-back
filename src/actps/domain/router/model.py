from datetime import datetime

from src.actps.core.base_entity import AbstractBaseEntity


class Router(AbstractBaseEntity):

    def __init__(
        self,
        model_name: str,
        ip_address: str,
        hostname: str,
        created_at: datetime = None,
        id: int = None,
        reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._model_name = model_name
        self._ip_address = ip_address
        self._hostname = hostname
        self._created_at = created_at or datetime.utcnow()

    @property
    def id(self) -> int:
        return self._id

    @property
    def ip_address(self) -> str:
        return self._ip_address

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def created_at(self) -> datetime:
        return self._created_at

