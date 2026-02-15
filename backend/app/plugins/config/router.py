from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import RestaurantConfigOut, RestaurantConfigUpsert
from .service import get_or_create_config, upsert_config

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "config"}


@router.get("/restaurant", response_model=RestaurantConfigOut)
async def get_restaurant_config(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await get_or_create_config(session, tenant_id)


@router.put("/restaurant", response_model=RestaurantConfigOut)
async def put_restaurant_config(
    payload: RestaurantConfigUpsert, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await upsert_config(session, tenant_id, payload)

