from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import InvoiceCreate, InvoiceOut
from .service import create_invoice, list_invoices

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "invoices"}


@router.get("/invoices", response_model=list[InvoiceOut])
async def get_invoices(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_invoices(session, tenant_id)


@router.post("/invoices", response_model=InvoiceOut, status_code=status.HTTP_201_CREATED)
async def post_invoice(
    payload: InvoiceCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_invoice(session, tenant_id, payload)
