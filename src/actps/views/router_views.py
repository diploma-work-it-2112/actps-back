from sqlalchemy import text
from typing import List

from src.actps.gateway.schemas import RouterResponse
from src.actps.integrations.postgres.engine import AsyncEngine
from src.actps.gateway.converter import RouterConverter


class RouterViews:

    @classmethod
    async def get_router_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> RouterResponse:
        async with engine.begin() as conn:
            router_row = (await conn.execute(
                text("""
                    select 
                        *
                    from router
                    where pc.id=:id
                """), {
                    "id": id
                }
            )).one()

        return RouterConverter.row_to_router(router=router_row)


    @classmethod
    async def get_all_routers_view(
            cls,
            engine: AsyncEngine
    ) -> List[RouterResponse]:
        async with engine.begin() as conn:
            router_rows = (await conn.execute(
                text("""
                    select 
                        *
                    from router
                """
                )
            )).all()

        return RouterConverter.row_to_router_list(routers=router_rows)

