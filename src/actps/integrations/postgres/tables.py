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
    Column("hostname", String(256), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False)
)
