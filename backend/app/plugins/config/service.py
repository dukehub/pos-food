from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import RestaurantConfig
from .schemas import RestaurantConfigUpsert


def _clean(value: str | None) -> str:
    return (value or "").strip()


def _apply_payload(config: RestaurantConfig, payload: RestaurantConfigUpsert) -> None:
    config.name = _clean(payload.name)
    config.slug = _clean(payload.slug)
    config.currency = _clean(payload.currency) or "USD"
    config.locale = _clean(payload.locale) or "fr"

    config.address = _clean(payload.address)
    config.phone = _clean(payload.phone)
    config.email = _clean(payload.email)

    config.tax_nif = _clean(payload.tax_nif)
    config.tax_rc = _clean(payload.tax_rc)
    config.tax_ai = _clean(payload.tax_ai)

    config.logo_url = _clean(payload.logo_url)
    config.background_image_url = _clean(payload.background_image_url)
    config.background_image_secondary_url = _clean(payload.background_image_secondary_url)

    config.location_label = _clean(payload.location_label)
    config.city = _clean(payload.city)
    config.country = _clean(payload.country)
    config.postal_code = _clean(payload.postal_code)
    config.latitude = _clean(payload.latitude)
    config.longitude = _clean(payload.longitude)
    config.is_active = True


async def get_or_create_config(session: AsyncSession, tenant_id: str) -> RestaurantConfig:
    row = await session.execute(
        select(RestaurantConfig).where(RestaurantConfig.tenant_id == tenant_id)
    )
    config = row.scalar_one_or_none()
    if config:
        return config

    config = RestaurantConfig(tenant_id=tenant_id, is_active=True)
    session.add(config)
    await session.commit()
    await session.refresh(config)
    return config


async def upsert_config(
    session: AsyncSession, tenant_id: str, payload: RestaurantConfigUpsert
) -> RestaurantConfig:
    config = await get_or_create_config(session, tenant_id)
    _apply_payload(config, payload)
    await session.commit()
    await session.refresh(config)
    return config

