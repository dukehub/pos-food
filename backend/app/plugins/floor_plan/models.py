import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import relationship

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class TableStatus(str, enum.Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    CLEANING = "CLEANING"


class FloorPlanZone(Base):
    __tablename__ = "floor_plan_zone"
    __table_args__ = (
        UniqueConstraint("tenant_id", "name", name="uq_floor_plan_zone_tenant_name"),
        Index("ix_floor_plan_zone_tenant_order", "tenant_id", "display_order"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(80), nullable=False)
    display_order = Column(Integer, nullable=False, default=0)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    tables = relationship("FloorPlanTable", back_populates="zone")


class FloorPlanTable(Base):
    __tablename__ = "floor_plan_table"
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_floor_plan_table_tenant_code"),
        Index("ix_floor_plan_table_tenant_zone", "tenant_id", "zone_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    zone_id = Column(String(36), ForeignKey("floor_plan_zone.id"), nullable=True)
    code = Column(String(40), nullable=False)
    qr_code = Column(String(128), nullable=True)
    capacity = Column(Integer, nullable=False, default=4)
    status = Column(Enum(TableStatus), nullable=False, default=TableStatus.FREE)
    current_server_id = Column(String(36), nullable=True)
    parent_table_id = Column(String(36), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    zone = relationship("FloorPlanZone", back_populates="tables")

