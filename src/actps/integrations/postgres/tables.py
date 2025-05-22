from enum import unique
from sqlalchemy import (
    String,
    Table,
    Column,
    BigInteger,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import registry 


mapper_registry = registry()


personal_computer = Table(
    "personal_computer",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("ip_address", String(256), nullable=False),
    Column("hostname", String(256), nullable=False, unique=True),
    Column("router_id", ForeignKey("router.id", ondelete="CASCADE"), nullable=True),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

router = Table(
    "router",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("model_name", String(256), nullable=False),
    Column("ip_address", String(256), nullable=False),
    Column("color", String(8), nullable=False),
    Column("group_name", String(256), nullable=True),
    Column("hostname", String(256), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)

package_log = Table(
    "package_log",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("message", String(512), nullable=True),
    # Column("type", Enum)
    Column("ip_source", String(256), nullable=False),
    Column("ip_destination", String(256), nullable=False),
    Column("mac_source", String(256), nullable=False),
    Column("mac_destination", String(256), nullable=False),
    Column("port_source", String(256), nullable=False),
    Column("port_destination", String(256), nullable=False),
    Column("web_host_name", String(256), nullable=True),
    Column("pc_id", ForeignKey("personal_computer.id", ondelete="CASCADE"), nullable=True),
    Column("time", DateTime(timezone=True), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=True)
)

proces_log = Table(
    "proces_log",
    mapper_registry.metadata,
    Column("id", BigInteger, primary_key=True, index=True, autoincrement=True),
    Column("name", String(512), nullable=False),
    Column("path", String(512), nullable=False),
    Column("pred", String(512), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=True)
)
