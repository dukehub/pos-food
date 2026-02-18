from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import DevicePrinterCreate, DevicePrinterOut, DevicePrinterUpdate
from .service import create_printer, list_printers, update_printer, delete_printer

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "printer"}


@router.get("/printers", response_model=list[DevicePrinterOut])
async def get_printers(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_printers(session, tenant_id)


@router.post("/printers", response_model=DevicePrinterOut, status_code=status.HTTP_201_CREATED)
async def post_printer(
    payload: DevicePrinterCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    tenant_id = _require_tenant()
    return await create_printer(session, tenant_id, payload)


@router.put("/printers/{printer_id}", response_model=DevicePrinterOut)
async def put_printer(
    printer_id: str,
    payload: DevicePrinterUpdate,
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await update_printer(session, tenant_id, printer_id, payload)


@router.delete("/printers/{printer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_printer_endpoint(
    printer_id: str, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    await delete_printer(session, tenant_id, printer_id)

