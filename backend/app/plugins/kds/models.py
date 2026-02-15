import uuid

from sqlalchemy import Boolean, Column, DateTime, Index, Integer, String, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class KdsScreen(Base):
    __tablename__ = "device_kds"
    __table_args__ = (
        Index("ix_device_kds_tenant_name", "tenant_id", "name"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(100), nullable=False)
    ip_address = Column(String(64), nullable=True)
    port = Column(Integer, nullable=False, default=3000)
    location = Column(String(120), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

