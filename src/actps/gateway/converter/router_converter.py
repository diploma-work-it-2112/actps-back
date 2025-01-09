from sqlalchemy import Row
from typing import List

from src.actps.domain.pc import PC
from src.actps.gateway.schemas import RouterResponse


class RouterConverter:

    @classmethod
    def row_to_router(cls, router: Row) -> RouterResponse:
        return RouterResponse(
            id=router.id,
            model_name=router.model_name,
            ip_address=router.ip_address,
            hostname=router.hostname,
            created_at=router.created_at
        )

    @classmethod
    def row_to_router_list(cls, routers) -> List[RouterResponse]:
        return [cls.row_to_router(router) for router in routers]

    @classmethod
    def model_to_rotuer(cls, router: PC) -> RouterResponse:
        return PCResponse(
            id=pc.id,
            ip_address=pc.ip_address,
            hostname=pc.hostname,
            router_id=pc.router_id,
            created_at=pc.created_at
        )

    @classmethod
    def model_to_router_list(cls, pcs: List[PC]) -> List[RouterResponse]:
        return [cls.model_to_pc(pc) for pc in pcs]

