import colorsys

from datetime import datetime

from src.actps.core.base_entity import AbstractBaseEntity
from src.actps.domain.pc.personal_computer import PC


class Router(AbstractBaseEntity):

    def __init__(
        self,
        model_name: str,
        ip_address: str,
        hostname: str,
        color: str = None,
        color_index: int = None,
        group_name: str = None,
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
        self._color = color or self.generate_color(color_index)
        self._group_name = group_name

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
    
    @property
    def color(self) -> str:
        return self._color

    @property 
    def group_name(self) -> str:
        return self._group_name

    def generate_color(self, index, saturation=0.5, brightness=0.95):
        golden_ratio_conjugate = 0.618033988749895
        h = (index * golden_ratio_conjugate) % 1  
        r, g, b = colorsys.hsv_to_rgb(h, saturation, brightness)
        return f"#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}"

    def update(self, new_model_name=None, new_color=None, new_group_name=None):
        self._model_name = new_model_name or self._model_name
        self._color = new_color or self._color
        self._group_name = new_group_name or self._group_name
