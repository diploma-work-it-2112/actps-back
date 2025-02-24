from datetime import datetime 

from src.actps.core.base_entity import AbstractBaseEntity


class PackageLog(AbstractBaseEntity):

    def __init__(
        self,
        ip_source: str,
        ip_destination: str,
        mac_source: str,
        mac_destination: str,
        port_source: str,
        port_destinatin: str,
        time: datetime,
        web_host_name: str = None,
        pc_id: int = None,
        message: str = None,
        id: int = None,
        created_at: datetime = None
    ):
        self._id = id
        self._message = message
        self._pc_id = pc_id 
        self._web_host_name = web_host_name
        self._ip_source = ip_source
        self._ip_destination = ip_destination 
        self._mac_source = mac_source
        self._mac_destinations = mac_destination
        self._port_source = port_source
        self._port_destination = port_destinatin
        self._time = time
        self._created_at = created_at or datetime.utcnow()


    @property
    def id(self) -> int:
        return self._id

    @property
    def message(self) -> str:
        return self._message

    @property
    def pc_id(self) -> int:
        return self._pc_id

    @property
    def web_host_name(self) -> str:
        return self._web_host_name

    @property
    def ip_source(self) -> str:
        return self._ip_source

    @property
    def ip_destination(self) -> str:
        return self._ip_destination

    @property
    def mac_source(self) -> str:
        return self._mac_source

    @property
    def mac_destination(self) -> str:
        return self._mac_destinations

    @property
    def port_source(self) -> str:
        return self._port_source

    @property
    def port_destination(self) -> str:
        return self._port_destination

    @property
    def time(self) -> datetime:
        return self._time

    @property
    def created_at(self) -> datetime:
        return self._created_at
