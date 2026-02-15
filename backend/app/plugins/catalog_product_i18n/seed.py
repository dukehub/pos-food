# app/plugins/catalog_product_i18n/seed.py
from sqlalchemy import select
from app.core.plugins.models import Permission  # si tu as une table permission

async def seed(session, tenant_id: str) -> None:
    # créer permissions si n'existent pas
    wanted = ["catalog_product_i18n.read", "catalog_product_i18n.write"]
    existing = (await session.execute(select(Permission.code).where(Permission.tenant_id == tenant_id))).scalars().all()
    missing = [p for p in wanted if p not in set(existing)]
    for code in missing:
        session.add(Permission(tenant_id=tenant_id, code=code, label=code))
    await session.flush()
