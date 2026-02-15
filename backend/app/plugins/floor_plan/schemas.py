import enum

from pydantic import BaseModel, ConfigDict, Field


class TableStatus(str, enum.Enum):
    FREE = "FREE"
    OCCUPIED = "OCCUPIED"
    CLEANING = "CLEANING"


class FloorZoneCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    display_order: int = 0
    is_active: bool = True


class FloorZoneOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    display_order: int
    is_active: bool


class DiningTableCreate(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    zone_id: str | None = None
    qr_code: str | None = Field(default=None, max_length=128)
    capacity: int = Field(default=4, ge=1, le=20)
    status: TableStatus = TableStatus.FREE
    current_server_id: str | None = None
    parent_table_id: str | None = None
    is_active: bool = True


class DiningTableOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    zone_id: str | None
    code: str
    qr_code: str | None
    capacity: int
    status: TableStatus
    current_server_id: str | None
    parent_table_id: str | None
    is_active: bool

