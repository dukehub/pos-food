from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import (
    Category,
    Product,
    ProductVariant,
    ModifierGroup,
    ModifierItem,
)
from .schemas import (
    CategoryCreate,
    CategoryUpdate,
    ProductCreate,
    ProductUpdate,
    ModifierGroupCreate,
    ModifierGroupUpdate,
)

# --- Category ---

async def list_categories(session: AsyncSession, tenant_id: str) -> list[Category]:
    stmt = (
        select(Category)
        .where(Category.tenant_id == tenant_id)
        .order_by(Category.sort_order, Category.name)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def create_category(session: AsyncSession, tenant_id: str, payload: CategoryCreate) -> Category:
    # Slug uniqueness check
    existing = await session.execute(
        select(Category).where(Category.tenant_id == tenant_id, Category.slug == payload.slug)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Category slug already exists")

    category = Category(tenant_id=tenant_id, **payload.model_dump())
    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category

async def update_category(session: AsyncSession, tenant_id: str, category_id: str, payload: CategoryUpdate) -> Category:
    category = await session.get(Category, category_id)
    if not category or category.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Category not found")

    data = payload.model_dump(exclude_unset=True)
    if "slug" in data and data["slug"] != category.slug:
         existing = await session.execute(
            select(Category).where(Category.tenant_id == tenant_id, Category.slug == data["slug"])
        )
         if existing.scalar_one_or_none():
            raise HTTPException(status_code=409, detail="Category slug already exists")

    for key, value in data.items():
        setattr(category, key, value)
    
    await session.commit()
    await session.refresh(category)
    return category

async def delete_category(session: AsyncSession, tenant_id: str, category_id: str):
    category = await session.get(Category, category_id)
    if not category or category.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(category)
    await session.commit()

# --- Modifier Group ---

async def list_modifier_groups(session: AsyncSession, tenant_id: str) -> list[ModifierGroup]:
    stmt = (
        select(ModifierGroup)
        .options(selectinload(ModifierGroup.items))
        .where(ModifierGroup.tenant_id == tenant_id)
        .order_by(ModifierGroup.sort_order, ModifierGroup.name)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def create_modifier_group(session: AsyncSession, tenant_id: str, payload: ModifierGroupCreate) -> ModifierGroup:
    existing = await session.execute(
        select(ModifierGroup).where(ModifierGroup.tenant_id == tenant_id, ModifierGroup.code == payload.code)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Modifier Group code already exists")

    # Create Group
    group_data = payload.model_dump(exclude={"items"})
    group = ModifierGroup(tenant_id=tenant_id, **group_data)
    session.add(group)
    
    # Create Items
    for item_data in payload.items:
        item = ModifierItem(tenant_id=tenant_id, group=group, **item_data.model_dump())
        session.add(item)

    await session.commit()
    await session.refresh(group, attribute_names=["items"])
    return group

async def update_modifier_group(session: AsyncSession, tenant_id: str, group_id: str, payload: ModifierGroupUpdate) -> ModifierGroup:
    group = await session.get(ModifierGroup, group_id)
    if not group or group.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Modifier Group not found")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(group, key, value)
    
    await session.commit()
    await session.refresh(group)
    # Re-fetch items if needed, but update mostly touches main fields
    return group

async def delete_modifier_group(session: AsyncSession, tenant_id: str, group_id: str):
    group = await session.get(ModifierGroup, group_id)
    if not group or group.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Modifier Group not found")
    await session.delete(group)
    await session.commit()

# --- Product ---

async def list_products(session: AsyncSession, tenant_id: str, category_id: str | None = None) -> list[Product]:
    stmt = (
        select(Product)
        .options(selectinload(Product.variants), selectinload(Product.modifier_groups))
        .where(Product.tenant_id == tenant_id)
    )
    if category_id:
        stmt = stmt.where(Product.category_id == category_id)
    
    stmt = stmt.order_by(Product.sort_order, Product.name)
    result = await session.execute(stmt)
    return list(result.scalars().all())

async def get_product(session: AsyncSession, tenant_id: str, product_id: str) -> Product:
    stmt = (
        select(Product)
        .options(
            selectinload(Product.variants).selectinload(ProductVariant.modifier_groups),
            selectinload(Product.modifier_groups)
        )
        .where(Product.id == product_id, Product.tenant_id == tenant_id)
    )
    result = await session.execute(stmt)
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def create_product(session: AsyncSession, tenant_id: str, payload: ProductCreate) -> Product:
    # 1. Create Product
    product_data = payload.model_dump(exclude={"variants", "modifier_group_ids"})
    product = Product(tenant_id=tenant_id, **product_data)
    
    # 2. Attach Modifier Groups (Product Level)
    if payload.modifier_group_ids:
        # Fetch groups
        groups_stmt = select(ModifierGroup).where(
            ModifierGroup.id.in_(payload.modifier_group_ids),
            ModifierGroup.tenant_id == tenant_id
        )
        groups = (await session.execute(groups_stmt)).scalars().all()
        product.modifier_groups = list(groups)

    session.add(product)
    
    # 3. Create Variants
    for v_payload in payload.variants:
        v_data = v_payload.model_dump(exclude={"modifier_group_ids"})
        variant = ProductVariant(tenant_id=tenant_id, product=product, **v_data)
        
        # Attach Modifier Groups (Variant Level)
        if v_payload.modifier_group_ids:
            v_groups_stmt = select(ModifierGroup).where(
                ModifierGroup.id.in_(v_payload.modifier_group_ids),
                ModifierGroup.tenant_id == tenant_id
            )
            v_groups = (await session.execute(v_groups_stmt)).scalars().all()
            variant.modifier_groups = list(v_groups)
        
        session.add(variant)

    await session.commit()
    await session.refresh(product, attribute_names=["variants", "modifier_groups"])
    return product

async def update_product(session: AsyncSession, tenant_id: str, product_id: str, payload: ProductUpdate) -> Product:
    product = await get_product(session, tenant_id, product_id)
    
    data = payload.model_dump(exclude_unset=True, exclude={"modifier_group_ids"})
    for key, value in data.items():
        setattr(product, key, value)

    if payload.modifier_group_ids is not None:
         groups_stmt = select(ModifierGroup).where(
            ModifierGroup.id.in_(payload.modifier_group_ids),
            ModifierGroup.tenant_id == tenant_id
        )
         groups = (await session.execute(groups_stmt)).scalars().all()
         product.modifier_groups = list(groups)

    await session.commit()
    await session.refresh(product)
    return product

async def delete_product(session: AsyncSession, tenant_id: str, product_id: str):
    product = await session.get(Product, product_id)
    if not product or product.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Product not found")
    await session.delete(product)
    await session.commit()
