from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.plugins.app_settings.models import SettingScope, SettingValueType


class AppSettingBase(BaseModel):
    scope: SettingScope = Field(default=SettingScope.TENANT)
    module: str = Field(default="core", max_length=60)
    key: str = Field(..., max_length=120)
    value_json: Any = Field(default_factory=dict)
    value_type: SettingValueType = Field(default=SettingValueType.ANY)
    description: Optional[str] = Field(None, max_length=255)
    is_active: bool = True


class AppSettingCreate(AppSettingBase):
    pass


class AppSettingUpdate(BaseModel):
    value_json: Optional[Any] = None
    value_type: Optional[SettingValueType] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class AppSettingRead(AppSettingBase):
    id: str
    tenant_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AppSettingBulkUpdate(BaseModel):
    settings: List[AppSettingCreate]
