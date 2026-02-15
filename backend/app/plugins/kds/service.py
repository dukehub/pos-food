from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import KdsScreen
from .schemas import KdsScreenCreate


async def list_kds(session: AsyncSession, tenant_id: str) -> list[KdsScreen]:
    rows = await session.execute(
        select(KdsScreen)
        .where(KdsScreen.tenant_id == tenant_id)
        .order_by(KdsScreen.name.asc())
    )
    return list(rows.scalars().all())


async def create_kds(
    session: AsyncSession, tenant_id: str, payload: KdsScreenCreate
) -> KdsScreen:
    existing = await session.execute(
        select(KdsScreen.id).where(
            KdsScreen.tenant_id == tenant_id,
            KdsScreen.name == payload.name,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="KDS name already exists for tenant")

    kds = KdsScreen(
        tenant_id=tenant_id,
        name=payload.name,
        ip_address=payload.ip_address,
        port=payload.port,
        location=payload.location,
        is_active=payload.is_active,
    )
    session.add(kds)
    await session.commit()
    await session.refresh(kds)
    return kds

