import enum

from pydantic import BaseModel, ConfigDict, Field


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SERVER = "serveur"
    POS = "pos"


class StaffUserCreate(BaseModel):
    username: str = Field(min_length=1, max_length=80)
    full_name: str | None = Field(default=None, max_length=120)
    pin_code: str | None = Field(default=None, max_length=12)
    role: UserRole = UserRole.SERVER
    language: str = Field(default="fr", max_length=10)
    avatar_url: str | None = Field(default=None, max_length=255)
    is_active: bool = True


class StaffUserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    tenant_id: str
    username: str
    full_name: str | None
    pin_code: str | None
    role: UserRole
    language: str
    avatar_url: str | None
    is_active: bool
