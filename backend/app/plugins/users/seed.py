from sqlalchemy import select

from app.core.plugins.models import Permission


async def seed(session, tenant_id: str) -> None:
    wanted = [
        "users.read",
        "users.write",
    ]
    existing = (
        await session.execute(
            select(Permission.code).where(Permission.tenant_id == tenant_id)
        )
    ).scalars().all()
    missing = [code for code in wanted if code not in set(existing)]
    for code in missing:
        session.add(Permission(tenant_id=tenant_id, code=code, label=code))
    await session.flush()
