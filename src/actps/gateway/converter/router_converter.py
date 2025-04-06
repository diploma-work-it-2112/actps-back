from sqlalchemy import Row
from typing import List

from src.actps.domain.pc import PC
from src.actps.gateway.schemas import RouterResponse
from src.actps.gateway.schemas.personal_computer_schemas import PCResponse


class RouterConverter:

    @classmethod
    def row_to_router(cls, router: Row) -> RouterResponse:
        return RouterResponse(
            id=router.router_id,
            model_name=router.model_name,
            ip_address=router.router_ip,
            hostname=router.router_hostname,
            created_at=router.router_created_at,
            color=router.router_color,
            group_name=router.router_group_name,
            computers=[
                PCResponse(
                    id=computer["computer_id"],
                    ip_address=computer["computer_ip"],
                    hostname=computer["computer_hostname"],
                    router_id=router.router_id,
                    created_at=computer["computer_created_at"]
                ) for computer in router.computers
            ] if router.computers is not None else []
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

