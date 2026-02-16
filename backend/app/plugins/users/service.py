from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security.utils import get_password_hash
from .models import StaffUser
from .schemas import StaffUserCreate


async def list_users(session: AsyncSession, tenant_id: str) -> list[StaffUser]:
    rows = await session.execute(
        select(StaffUser)
        .where(StaffUser.tenant_id == tenant_id)
        .order_by(StaffUser.username.asc())
    )
    return list(rows.scalars().all())


async def create_user(
    session: AsyncSession, tenant_id: str, payload: StaffUserCreate
) -> StaffUser:
    existing = await session.execute(
        select(StaffUser.id).where(
            StaffUser.tenant_id == tenant_id,
            StaffUser.username == payload.username,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Username already exists for tenant")
    
    # Hash the PIN or use default
    pwd_hash = get_password_hash(payload.pin_code) if payload.pin_code else get_password_hash("0000")

    user = StaffUser(
        tenant_id=tenant_id,
        username=payload.username,
        full_name=payload.full_name,
        password_hash=pwd_hash,
        role=payload.role,
        language=payload.language,
        avatar_url=payload.avatar_url,
        is_active=payload.is_active,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
