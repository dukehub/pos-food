import uuid

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Index, Integer, String, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


from app.plugins.devices.models import Device


class KdsScreen(Device):
    __tablename__ = "device_kds"
    # Parent 'device' table already has relevant indexes.
    __table_args__ = ()

    id = Column(String(36), ForeignKey("device.id", ondelete="CASCADE"), primary_key=True)

    port = Column(Integer, nullable=False, default=3000)

    __mapper_args__ = {"polymorphic_identity": "kds"}

