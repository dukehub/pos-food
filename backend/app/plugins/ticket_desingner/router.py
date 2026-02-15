from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import TicketTemplateCreate, TicketTemplateOut
from .service import create_template, list_templates

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "ticket_desingner"}


@router.get("/templates", response_model=list[TicketTemplateOut])
async def get_templates(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_templates(session, tenant_id)


@router.post("/templates", response_model=TicketTemplateOut, status_code=status.HTTP_201_CREATED)
async def post_template(
    payload: TicketTemplateCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_template(session, tenant_id, payload)
