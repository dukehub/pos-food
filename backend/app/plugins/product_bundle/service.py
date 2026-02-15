from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import ProductBundleItem
from .schemas import ProductBundleItemCreate


async def list_bundles(
    session: AsyncSession, tenant_id: str, parent_product_id: str | None = None
) -> list[ProductBundleItem]:
    stmt = select(ProductBundleItem).where(ProductBundleItem.tenant_id == tenant_id)
    if parent_product_id:
        stmt = stmt.where(ProductBundleItem.parent_product_id == parent_product_id)
    rows = await session.execute(
        stmt.order_by(
            ProductBundleItem.parent_product_id.asc(),
            ProductBundleItem.child_product_id.asc(),
        )
    )
    return list(rows.scalars().all())


async def create_bundle_item(
    session: AsyncSession, tenant_id: str, payload: ProductBundleItemCreate
) -> ProductBundleItem:
    if payload.parent_product_id == payload.child_product_id:
        raise HTTPException(status_code=400, detail="Parent and child product must be different")

    existing = await session.execute(
        select(ProductBundleItem.id).where(
            ProductBundleItem.tenant_id == tenant_id,
            ProductBundleItem.parent_product_id == payload.parent_product_id,
            ProductBundleItem.child_product_id == payload.child_product_id,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Bundle item already exists for tenant")

    item = ProductBundleItem(
        tenant_id=tenant_id,
        parent_product_id=payload.parent_product_id,
        child_product_id=payload.child_product_id,
        quantity=payload.quantity,
        is_active=payload.is_active,
    )
    session.add(item)
    await session.commit()
    await session.refresh(item)
    return item
