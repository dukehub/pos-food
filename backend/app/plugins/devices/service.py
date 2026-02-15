from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Device
from .schemas import DeviceCreate


async def list_devices(session: AsyncSession, tenant_id: str) -> list[Device]:
    rows = await session.execute(
        select(Device)
        .where(Device.tenant_id == tenant_id)
        .order_by(Device.name.asc())
    )
    return list(rows.scalars().all())


async def create_device(
    session: AsyncSession, tenant_id: str, payload: DeviceCreate
) -> Device:
    existing = await session.execute(
        select(Device.id).where(
            Device.tenant_id == tenant_id,
            Device.name == payload.name,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Device name already exists for tenant")

    device = Device(
        tenant_id=tenant_id,
        name=payload.name,
        device_type=payload.device_type.strip() or "generic",
        identifier=(payload.identifier or "").strip() or None,
        location=(payload.location or "").strip() or None,
        ip_address=(payload.ip_address or "").strip() or None,
        is_active=payload.is_active,
    )
    session.add(device)
    await session.commit()
    await session.refresh(device)
    return device

