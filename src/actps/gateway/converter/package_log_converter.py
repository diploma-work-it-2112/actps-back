from sqlalchemy import Row 
from typing import List 

from src.actps.domain.logs import PackageLog
from src.actps.gateway.schemas import PackageLogResponse


class PackageLogConverter:

    @classmethod
    def row_to_package_log(cls, pkg: Row) -> PackageLogResponse:
        return PackageLogResponse(
            id=pkg.id,
            message=pkg.message,
            pc_id=pkg.pc_id,
            web_host_name=pkg.web_host_name,
            ip_source=pkg.ip_source,
            ip_destination=pkg.ip_destination,
            mac_source=pkg.mac_source,
            mac_destination=pkg.mac_destination,
            port_source=pkg.port_source,
            port_destination=pkg.port_destination,
            time=pkg.time,
            created_at=pkg.created_at
        )

    @classmethod
    def row_to_package_log_list(cls, pkgs) -> List[PackageLogResponse]:
        return [cls.row_to_package_log(pkg) for pkg in pkgs]

    @classmethod
    def model_to_package_log(cls, pkg: PackageLog) -> PackageLogResponse:
        return PackageLogResponse(
            id=pkg.id,
            message=pkg.message,
            pc_id=pkg.pc_id,
            web_host_name=pkg.web_host_name,
            ip_source=pkg.ip_source,
            ip_destination=pkg.ip_destination,
            mac_source=pkg.mac_source,
            mac_destination=pkg.mac_destination,
            port_source=pkg.port_source,
            port_destination=pkg.port_destination,
            time=pkg.time,
            created_at=pkg.created_at
        )

    @classmethod
    def model_to_package_log_list(cls, pkgs: List[PackageLog]) -> List[PackageLogResponse]:
        return [cls.model_to_package_log(pkg) for pkg in pkgs]

