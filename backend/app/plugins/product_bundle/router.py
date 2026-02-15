from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import ProductBundleItemCreate, ProductBundleItemOut
from .service import create_bundle_item, list_bundles

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "product_bundle"}


@router.get("/bundles", response_model=list[ProductBundleItemOut])
async def get_bundles(
    parent_product_id: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await list_bundles(session, tenant_id, parent_product_id=parent_product_id)


@router.post("/bundles", response_model=ProductBundleItemOut, status_code=status.HTTP_201_CREATED)
async def post_bundle(
    payload: ProductBundleItemCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_bundle_item(session, tenant_id, payload)
