from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.plugins.app_settings.models import AppSetting
from app.plugins.app_settings.schemas import AppSettingCreate, AppSettingUpdate


class AppSettingsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, tenant_id: str) -> List[AppSetting]:
        query = select(AppSetting).where(AppSetting.tenant_id == tenant_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_key(self, tenant_id: str, key: str, scope: str = "tenant") -> Optional[AppSetting]:
        query = select(AppSetting).where(
            AppSetting.tenant_id == tenant_id,
            AppSetting.key == key,
            AppSetting.scope == scope
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_by_module(self, tenant_id: str, module: str) -> List[AppSetting]:
        query = select(AppSetting).where(
            AppSetting.tenant_id == tenant_id,
            AppSetting.module == module
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, tenant_id: str, schema: AppSettingCreate) -> AppSetting:
        db_obj = AppSetting(
            tenant_id=tenant_id,
            scope=schema.scope,
            module=schema.module,
            key=schema.key,
            value_json=schema.value_json,
            value_type=schema.value_type,
            description=schema.description,
            is_active=schema.is_active
        )
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: AppSetting, schema: AppSettingUpdate) -> AppSetting:
        if schema.value_json is not None:
            db_obj.value_json = schema.value_json
        if schema.value_type is not None:
            db_obj.value_type = schema.value_type
        if schema.description is not None:
            db_obj.description = schema.description
        if schema.is_active is not None:
            db_obj.is_active = schema.is_active
        
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def upsert(self, tenant_id: str, schema: AppSettingCreate) -> AppSetting:
        existing = await self.get_by_key(tenant_id, schema.key, schema.scope)
        if existing:
            # Update existing
            update_data = AppSettingUpdate(
                value_json=schema.value_json,
                value_type=schema.value_type,
                description=schema.description,
                is_active=schema.is_active
            )
            return await self.update(existing, update_data)
        else:
            return await self.create(tenant_id, schema)

    async def bulk_upsert(self, tenant_id: str, settings: List[AppSettingCreate]) -> List[AppSetting]:
        results = []
        for setting in settings:
            result = await self.upsert(tenant_id, setting)
            results.append(result)
        return results
