from datetime import datetime

class Warning:
    def __init__(
        self,
        hostname: str,
        type: str,
        message: str,
        created_at: datetime = None,
        id: int = None
    ):
        self._id = id
        self._hostname = hostname
        self._type = type
        self._message = message
        self._created_at = created_at or datetime.utcnow()

    @property
    def id(self) -> int:
        return self._id

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def type(self) -> str:
        return self._type

    @property
    def message(self) -> str:
        return self._message

    @property
    def created_at(self) -> datetime:
        return self._created_at

