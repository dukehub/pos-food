from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import OrderCreate, OrderOut, OrderUpdate
from .service import create_order, list_orders, update_order

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "orders"}


@router.get("/orders", response_model=list[OrderOut])
async def get_orders(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_orders(session, tenant_id)


@router.post("/orders", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
async def post_order(
    payload: OrderCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_order(session, tenant_id, payload)


@router.put("/orders/{order_id}", response_model=OrderOut)
async def put_order(
    order_id: str,
    payload: OrderUpdate,
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await update_order(session, tenant_id, order_id, payload)

