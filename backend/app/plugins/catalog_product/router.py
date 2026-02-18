from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id
from fastapi import HTTPException

from .schemas import (
    CategoryCreate, CategoryUpdate, CategoryOut,
    ModifierGroupCreate, ModifierGroupUpdate, ModifierGroupOut,
    ProductCreate, ProductUpdate, ProductOut
)
from .service import (
    list_categories, create_category, update_category, delete_category,
    list_modifier_groups, create_modifier_group, update_modifier_group, delete_modifier_group,
    list_products, get_product, create_product, update_product, delete_product
)

router = APIRouter()

def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id

@router.get("/health")
def health():
    return {"status": "ok", "service": "catalog_product"}

# --- Categories ---

@router.get("/categories", response_model=list[CategoryOut])
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await list_categories(session, _require_tenant())

@router.post("/categories", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def post_category(payload: CategoryCreate, session: AsyncSession = Depends(get_session)):
    return await create_category(session, _require_tenant(), payload)

@router.put("/categories/{category_id}", response_model=CategoryOut)
async def put_category(category_id: str, payload: CategoryUpdate, session: AsyncSession = Depends(get_session)):
    return await update_category(session, _require_tenant(), category_id, payload)

@router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_endpoint(category_id: str, session: AsyncSession = Depends(get_session)):
    await delete_category(session, _require_tenant(), category_id)

# --- Modifiers ---

@router.get("/modifiers", response_model=list[ModifierGroupOut])
async def get_modifiers(session: AsyncSession = Depends(get_session)):
    return await list_modifier_groups(session, _require_tenant())

@router.post("/modifiers", response_model=ModifierGroupOut, status_code=status.HTTP_201_CREATED)
async def post_modifier(payload: ModifierGroupCreate, session: AsyncSession = Depends(get_session)):
    return await create_modifier_group(session, _require_tenant(), payload)

@router.put("/modifiers/{group_id}", response_model=ModifierGroupOut)
async def put_modifier(group_id: str, payload: ModifierGroupUpdate, session: AsyncSession = Depends(get_session)):
    return await update_modifier_group(session, _require_tenant(), group_id, payload)

@router.delete("/modifiers/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_modifier(group_id: str, session: AsyncSession = Depends(get_session)):
    await delete_modifier_group(session, _require_tenant(), group_id)

# --- Products ---

@router.get("/products", response_model=list[ProductOut])
async def get_products(
    category_id: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session)
):
    return await list_products(session, _require_tenant(), category_id)

@router.get("/products/{product_id}", response_model=ProductOut)
async def get_product_detail(product_id: str, session: AsyncSession = Depends(get_session)):
    return await get_product(session, _require_tenant(), product_id)

@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def post_product(payload: ProductCreate, session: AsyncSession = Depends(get_session)):
    return await create_product(session, _require_tenant(), payload)

@router.put("/products/{product_id}", response_model=ProductOut)
async def put_product(product_id: str, payload: ProductUpdate, session: AsyncSession = Depends(get_session)):
    return await update_product(session, _require_tenant(), product_id, payload)

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_endpoint(product_id: str, session: AsyncSession = Depends(get_session)):
    await delete_product(session, _require_tenant(), product_id)
