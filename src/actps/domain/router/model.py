from datetime import datetime

from src.actps.core.base_entity import AbstractBaseEntity
from src.actps.domain.pc.personal_computer import PC


class Router(AbstractBaseEntity):

    def __init__(
        self,
        model_name: str,
        ip_address: str,
        hostname: str,
        computers: list[PC] = [],
        created_at: datetime = None,
        id: int = None,
        reference = None
    ):
        AbstractBaseEntity.__init__(self, reference)
        self._id = id
        self._model_name = model_name
        self._ip_address = ip_address
        self._computers = computers
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
    def computers(self) -> list:
        return self._computers

    @property
    def created_at(self) -> datetime:
        return self._created_at

