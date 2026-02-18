from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import CustomerCreate, CustomerOut, CustomerUpdate
from .service import create_customer, list_customers, update_customer, delete_customer

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "customers"}


@router.get("/customers", response_model=list[CustomerOut])
async def get_customers(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_customers(session, tenant_id)


@router.post("/customers", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
async def post_customer(
    payload: CustomerCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_customer(session, tenant_id, payload)


@router.put("/customers/{customer_id}", response_model=CustomerOut)
async def put_customer(
    customer_id: str,
    payload: CustomerUpdate,
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await update_customer(session, tenant_id, customer_id, payload)


@router.delete("/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_endpoint(
    customer_id: str, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    await delete_customer(session, tenant_id, customer_id)
