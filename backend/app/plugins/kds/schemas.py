from pydantic import BaseModel, ConfigDict, Field


class KdsScreenCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    ip_address: str | None = Field(default=None, max_length=64)
    port: int = Field(default=3000, ge=1, le=65535)
    location: str | None = Field(default=None, max_length=120)
    is_active: bool = True


class KdsScreenOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    name: str
    ip_address: str | None
    port: int
    location: str | None
    is_active: bool

