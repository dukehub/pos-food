from pydantic import BaseModel, ConfigDict, Field


class DeviceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    device_type: str = Field(default="generic", min_length=1, max_length=32)
    identifier: str | None = Field(default=None, max_length=120)
    location: str | None = Field(default=None, max_length=120)
    ip_address: str | None = Field(default=None, max_length=64)
    is_active: bool = True


class DeviceOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    device_type: str
    identifier: str | None
    location: str | None
    ip_address: str | None
    is_active: bool

