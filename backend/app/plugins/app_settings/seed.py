from sqlalchemy.ext.asyncio import AsyncSession
from app.plugins.app_settings.models import SettingScope, SettingValueType
from app.plugins.app_settings.schemas import AppSettingCreate
from app.plugins.app_settings.service import AppSettingsService

async def seed(session: AsyncSession, tenant_id: str) -> None:
    print(f"DEBUG: Seeding config for {tenant_id}")
    service = AppSettingsService(session)
    # 1. Check if restaurant info exists
    existing = await service.get_by_key(tenant_id, "restaurant_info")
    if not existing:
        print("DEBUG: Creating restaurant_info")
        # Create default restaurant config
        payload = AppSettingCreate(
            key="restaurant_info",
            value_json={
                "name": "My Restaurant",
                "currency": "USD",
                "locale": "fr",
                "tenant_id": tenant_id
            },
            scope=SettingScope.TENANT,
            value_type=SettingValueType.OBJECT,
            description="General restaurant configuration"
        )
        await service.upsert(tenant_id, payload)
    else:
        print("DEBUG: restaurant_info already exists")
