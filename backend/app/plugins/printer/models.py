import enum
from typing import Optional
from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey, Index, Integer, String
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.base import Base
from app.plugins.devices.models import Device


class PrinterType(str, enum.Enum):
    NETWORK = "network"
    WINDOWS_RAW = "windows"
    USB = "usb"
    BLUETOOTH = "bluetooth"


class DevicePrinter(Device):
    __tablename__ = "device_printer"
    # Parent 'device' table already indexes tenant_id+name.
    # We don't need to re-index here unless we duplicate columns.
    __table_args__ = ()

    id = Column(String(36), ForeignKey("device.id", ondelete="CASCADE"), primary_key=True)

    driver_type = Column(Enum(PrinterType), nullable=False, default=PrinterType.WINDOWS_RAW)
    system_printer_name = Column(String(120), nullable=True)
    # ip_address is inherited from Device
    port = Column(Integer, nullable=False, default=9100)
    paper_width = Column(Integer, nullable=False, default=80)

    __mapper_args__ = {"polymorphic_identity": "printer"}