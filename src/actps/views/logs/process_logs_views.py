from sqlalchemy import text
from typing import List 

from src.actps.gateway.converter.process_log_converter import ProcessLogConverter
from src.actps.integrations.postgres.engine import AsyncEngine 
from src.actps.gateway.schemas import PackageLogResponse
from src.actps.gateway.converter import PackageLogConverter


class ProcessLogViews:

    @classmethod
    async def get_process_log_by_name_view(
            cls,
            name: str,
            engine: AsyncEngine
    ) -> PackageLogResponse:
        async with engine.begin() as conn:
            pkg_row = (await conn.execute(
                text("""
                    select 
                        pkg.*
                    from proces_log pkg
                    where pkg.name = :name
                """),
                {"name": name}
            )).first()

        return ProcessLogConverter.row_to_process_log(row=pkg_row)

    @classmethod
    async def get_all_process_logs_view(
            cls,
            engine: AsyncEngine
    ) -> List[PackageLogResponse]:
        async with engine.begin() as conn:
            pkg_rows = (await conn.execute(
                text("""
                    select 
                        pkg.*
                    from proces_log pkg
                """)
            )).all()

        return ProcessLogConverter.row_to_process_log_list(rows=pkg_rows)


