from sqlalchemy import text
from typing import List

from src.actps.gateway.converter.warning_converter import WarningConverter
from src.actps.gateway.schemas.warning_schemas import WarningResponse
from src.actps.integrations.postgres.engine import AsyncEngine


class WarningViews:

    @classmethod
    async def get_warning_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> WarningResponse:
        async with engine.begin() as conn:
            warning_row = (await conn.execute(
                text("""
                    select 
                        w.*
                    from warning w
                    where w.id = :id
                """),
                {"id": id}
            )).one()

        return WarningConverter.row_to_warning(warning_row)

    @classmethod
    async def get_all_warnings_view(
            cls,
            engine: AsyncEngine
    ) -> List[WarningResponse]:
        async with engine.begin() as conn:
            warning_rows = (await conn.execute(
                text("""
                    select 
                        w.*
                    from warning w
                """)
            )).all()

        return WarningConverter.row_to_warning_list(warning_rows)

    @classmethod
    async def get_latest_warning_view(
            cls,
            engine: AsyncEngine
    ) -> WarningResponse:
        async with engine.begin() as conn:
            warning_row = (await conn.execute(
                text("""
                    select 
                        w.*
                    from warning w
                    order by w.created_at desc
                    limit 1
                """)
            )).one()

        return WarningConverter.row_to_warning(warning_row)

