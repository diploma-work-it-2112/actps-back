from uuid import uuid4
from abc import ABC


class AbstractBaseEntity(ABC):

    def __init__(self, reference=None):
        self._reference = reference or uuid4()

    def __eq__(self, __value: object) -> bool:
        return isinstance(type(__value), type(self)) and self._reference == __value._reference
    
    def __hash__(self) -> int:
        return hash(self.reference)
    
    @property
    def reference(self) -> uuid4:
        return self._reference
