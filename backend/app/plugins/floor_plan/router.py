from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.session import get_session
from app.core.tenancy.context import get_tenant_id

from .schemas import DiningTableCreate, DiningTableOut, FloorZoneCreate, FloorZoneOut
from .service import (
    create_table,
    create_zone,
    delete_table,
    delete_zone,
    list_tables,
    list_zones,
    update_table,
    update_zone,
)

router = APIRouter()


def _require_tenant() -> str:
    tenant_id = get_tenant_id()
    if not tenant_id or tenant_id == "public":
        raise HTTPException(status_code=403, detail="Tenant context required")
    return tenant_id


@router.get("/health")
def health():
    return {"status": "ok", "service": "floor_plan"}


@router.get("/zones", response_model=list[FloorZoneOut])
async def get_zones(session: AsyncSession = Depends(get_session)):
    tenant_id = _require_tenant()
    return await list_zones(session, tenant_id)


@router.post("/zones", response_model=FloorZoneOut, status_code=status.HTTP_201_CREATED)
async def post_zone(
    payload: FloorZoneCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_zone(session, tenant_id, payload)


@router.get("/tables", response_model=list[DiningTableOut])
async def get_tables(
    zone_id: str | None = Query(default=None),
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await list_tables(session, tenant_id, zone_id=zone_id)


@router.post("/tables", response_model=DiningTableOut, status_code=status.HTTP_201_CREATED)
async def post_table(
    payload: DiningTableCreate, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    return await create_table(session, tenant_id, payload)


@router.put("/zones/{zone_id}", response_model=FloorZoneOut)
async def put_zone(
    zone_id: str,
    payload: FloorZoneCreate,  # Using Create model for simplicity in service, or Update model if partial
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    # Note: service.update_zone expects FloorZoneCreate but we might want partial updates.
    # For now, let's assume full update or the service handles it. 
    # The service code I added uses payload.name checks.
    # Ideally should use FloorZoneUpdate schema with PATCH, but PUT is fine if full object or handled.
    # Let's use the type hint matching service.py for now.
    return await update_zone(session, tenant_id, zone_id, payload)


@router.delete("/zones/{zone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_zone_endpoint(
    zone_id: str, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    await delete_zone(session, tenant_id, zone_id)


@router.put("/tables/{table_id}", response_model=DiningTableOut)
async def put_table(
    table_id: str,
    payload: DiningTableCreate,
    session: AsyncSession = Depends(get_session),
):
    tenant_id = _require_tenant()
    return await update_table(session, tenant_id, table_id, payload)


@router.delete("/tables/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table_endpoint(
    table_id: str, session: AsyncSession = Depends(get_session)
):
    tenant_id = _require_tenant()
    await delete_table(session, tenant_id, table_id)

