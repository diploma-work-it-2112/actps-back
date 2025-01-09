from sqlalchemy import text
from typing import List

from src.actps.integrations.postgres.engine import AsyncEngine
from src.actps.gateway.schemas import PCResponse
from src.actps.gateway.converter import PCConverter


class PCViews:

    @classmethod
    async def get_pc_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> PCResponse:
        async with engine.begin() as conn:
            pc_row = (await conn.execute(
                text("""
                    select 
                        pc.*
                    from personal_computer pc
                    where pc.id=:id
                """), {
                    "id": id
                }
            )).one()

        return PCConverter.row_to_pc(pc=pc_row)


    @classmethod
    async def get_all_pcs_view(
            cls,
            engine: AsyncEngine
    ) -> List[PCResponse]:
        async with engine.begin() as conn:
            pc_rows = (await conn.execute(
                text("""
                    select 
                        pc.*
                    from personal_computer pc
                """
                )
            )).all()

        return PCConverter.row_to_pc_list(pcs=pc_rows)
