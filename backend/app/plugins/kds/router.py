from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import KdsScreenCreate, KdsScreenOut
from .service import create_kds, list_kds

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "kds"}


@router.get("/kds", response_model=list[KdsScreenOut])
async def get_kds(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_kds(session, tenant_id)


@router.post("/kds", response_model=KdsScreenOut, status_code=status.HTTP_201_CREATED)
async def post_kds(
    payload: KdsScreenCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_kds(session, tenant_id, payload)
