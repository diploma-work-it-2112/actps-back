from sqlalchemy import Row
from typing import List

from src.actps.gateway.schemas import PCResponse
from src.actps.domain.pc import PC


class PCConverter:

    @classmethod
    def row_to_pc(cls, pc: Row) -> PCResponse:
        return PCResponse(
            id=pc.id,
            ip_address=pc.ip_address,
            hostname=pc.hostname,
            router_id=pc.router_id,
            created_at=pc.created_at
        )

    @classmethod
    def row_to_pc_list(cls, pcs) -> List[PCResponse]:
        return [cls.row_to_pc(pc) for pc in pcs]

    @classmethod
    def model_to_pc(cls, pc: PC) -> PCResponse:
        return PCResponse(
            id=pc.id,
            ip_address=pc.ip_address,
            hostname=pc.hostname,
            router_id=pc.router_id,
            created_at=pc.created_at
        )

    @classmethod
    def model_to_pc_list(cls, pcs: List[PC]) -> List[PCResponse]:
        return [cls.model_to_pc(pc) for pc in pcs]
