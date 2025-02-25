from sqlalchemy import text
from typing import List 

from src.actps.integrations.postgres.engine import AsyncEngine 
from src.actps.gateway.schemas import PackageLogResponse
from src.actps.gateway.converter import PackageLogConverter


class PackageLogViews:

    @classmethod
    async def get_package_log_by_id_view(
            cls,
            id: int,
            engine: AsyncEngine
    ) -> PackageLogResponse:
        async with engine.begin() as conn:
            pkg_row = (await conn.execute(
                text("""
                    select 
                        pkg.*
                    from package_log pkg
                    where pkg.id = :id
                """),
                {"id": id}
            )).one()

        return PackageLogConverter.row_to_package_log(pkg=pkg_row)

    @classmethod
    async def get_all_package_logs_view(
            cls,
            engine: AsyncEngine
    ) -> List[PackageLogResponse]:
        async with engine.begin() as conn:
            pkg_rows = (await conn.execute(
                text("""
                    select 
                        pkg.*
                    from package_log pkg
                """)
            )).all()

        return PackageLogConverter.row_to_package_log_list(pkgs=pkg_rows)


    @classmethod
    async def get_package_log_by_pc_hostname_view(
            cls,
            pc_hostname: str,
            engine: AsyncEngine
    ) -> List[PackageLogResponse]:
        async with engine.begin() as conn:
            pkg_rows = (await conn.execute(
                text("""
                    select pkg.*
                    from package_log pkg
                    join personal_computer pc on pkg.pc_id = pc.id
                    where pc.hostname = :pc_hostname
                """),
                {"pc_hostname": pc_hostname}
            )).all()

        return PackageLogConverter.row_to_package_log_list(pkgs=pkg_rows)

