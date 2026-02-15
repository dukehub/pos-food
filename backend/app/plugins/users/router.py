from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import StaffUserCreate, StaffUserOut
from .service import create_user, list_users

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "users"}


@router.get("/users", response_model=list[StaffUserOut])
async def get_users(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_users(session, tenant_id)


@router.post("/users", response_model=StaffUserOut, status_code=status.HTTP_201_CREATED)
async def post_user(
    payload: StaffUserCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_user(session, tenant_id, payload)
