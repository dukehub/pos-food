from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import DeviceCreate, DeviceOut
from .service import create_device, list_devices

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "devices"}


@router.get("/devices", response_model=list[DeviceOut])
async def get_devices(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_devices(session, tenant_id)


@router.post("/devices", response_model=DeviceOut, status_code=status.HTTP_201_CREATED)
async def post_device(
    payload: DeviceCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_device(session, tenant_id, payload)

