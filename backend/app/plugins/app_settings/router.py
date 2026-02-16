from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id
from app.plugins.app_settings.schemas import (
    AppSettingCreate,
    AppSettingUpdate,
    AppSettingRead,
    AppSettingBulkUpdate
)
from app.plugins.app_settings.service import AppSettingsService

router = APIRouter()


async def get_service(session: AsyncSession = Depends(get_session)) -> AppSettingsService:
    return AppSettingsService(session)


@router.get("/", response_model=List[AppSettingRead])
async def list_settings(
    module: Optional[str] = Query(None),
    service: AppSettingsService = Depends(get_service)
):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is missing")
    
    if module:
        return await service.get_by_module(tenant_id, module)
    return await service.get_all(tenant_id)


@router.get("/{key}", response_model=AppSettingRead)
async def get_setting(
    key: str,
    scope: str = Query("tenant"),
    service: AppSettingsService = Depends(get_service)
):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is missing")
        
    setting = await service.get_by_key(tenant_id, key, scope)
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting


@router.put("/{key}", response_model=AppSettingRead)
async def update_setting_by_key(
    key: str,
    schema: AppSettingUpdate,
    scope: str = Query("tenant"),
    service: AppSettingsService = Depends(get_service)
):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is missing")

    existing = await service.get_by_key(tenant_id, key, scope)
    if not existing:
         raise HTTPException(status_code=404, detail="Setting not found")

    return await service.update(existing, schema)


@router.post("/", response_model=AppSettingRead)
async def upsert_setting(
    schema: AppSettingCreate,
    service: AppSettingsService = Depends(get_service)
):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is missing")
    
    # Force tenant_id from context just in case, though service handles it
    return await service.upsert(tenant_id, schema)


@router.put("/bulk", response_model=List[AppSettingRead])
async def bulk_upsert_settings(
    bulk_data: AppSettingBulkUpdate,
    service: AppSettingsService = Depends(get_service)
):
    tenant_id = get_tenant_id()
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Tenant ID is missing")

    return await service.bulk_upsert(tenant_id, bulk_data.settings)
