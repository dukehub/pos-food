import enum

from pydantic import BaseModel, ConfigDict, Field


class PrinterType(str, enum.Enum):
    NETWORK = "network"
    WINDOWS_RAW = "windows"
    USB = "usb"
    BLUETOOTH = "bluetooth"


class DevicePrinterCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    driver_type: PrinterType = PrinterType.WINDOWS_RAW
    system_printer_name: str | None = Field(default=None, max_length=120)
    ip_address: str | None = Field(default=None, max_length=64)
    port: int = Field(default=9100, ge=1, le=65535)
    paper_width: int = Field(default=80, ge=58, le=112)
    is_active: bool = True


class DevicePrinterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    driver_type: PrinterType
    system_printer_name: str | None
    ip_address: str | None
    port: int
    paper_width: int
    is_active: bool

