import uuid

from sqlalchemy import Boolean, Column, DateTime, Index, String, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class Device(Base):
    __tablename__ = "device"
    __table_args__ = (
        Index("ix_device_tenant_name", "tenant_id", "name"),
        Index("ix_device_tenant_type", "tenant_id", "device_type"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(100), nullable=False)
    device_type = Column(String(32), nullable=False, default="generic")
    identifier = Column(String(120), nullable=True)
    location = Column(String(120), nullable=True)
    ip_address = Column(String(64), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

