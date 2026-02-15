import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, Integer, String, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class PrinterType(str, enum.Enum):
    NETWORK = "network"
    WINDOWS_RAW = "windows"
    USB = "usb"
    BLUETOOTH = "bluetooth"


class DevicePrinter(Base):
    __tablename__ = "device_printer"
    __table_args__ = (
        Index("ix_device_printer_tenant_name", "tenant_id", "name"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(100), nullable=False)
    driver_type = Column(Enum(PrinterType), nullable=False, default=PrinterType.WINDOWS_RAW)
    system_printer_name = Column(String(120), nullable=True)
    ip_address = Column(String(64), nullable=True)
    port = Column(Integer, nullable=False, default=9100)
    paper_width = Column(Integer, nullable=False, default=80)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

