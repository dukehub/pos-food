from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import FloorPlanTable, FloorPlanZone
from .schemas import DiningTableCreate, FloorZoneCreate


async def list_zones(session: AsyncSession, tenant_id: str) -> list[FloorPlanZone]:
    rows = await session.execute(
        select(FloorPlanZone)
        .where(FloorPlanZone.tenant_id == tenant_id)
        .order_by(FloorPlanZone.display_order.asc(), FloorPlanZone.name.asc())
    )
    return list(rows.scalars().all())


async def create_zone(
    session: AsyncSession, tenant_id: str, payload: FloorZoneCreate
) -> FloorPlanZone:
    existing = await session.execute(
        select(FloorPlanZone.id).where(
            FloorPlanZone.tenant_id == tenant_id,
            FloorPlanZone.name == payload.name,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Zone name already exists for tenant")

    zone = FloorPlanZone(
        tenant_id=tenant_id,
        name=payload.name,
        display_order=payload.display_order,
        is_active=payload.is_active,
    )
    session.add(zone)
    await session.commit()
    await session.refresh(zone)
    return zone


async def list_tables(
    session: AsyncSession, tenant_id: str, zone_id: str | None = None
) -> list[FloorPlanTable]:
    stmt = select(FloorPlanTable).where(FloorPlanTable.tenant_id == tenant_id)
    if zone_id:
        stmt = stmt.where(FloorPlanTable.zone_id == zone_id)
    rows = await session.execute(stmt.order_by(FloorPlanTable.code.asc()))
    return list(rows.scalars().all())


async def create_table(
    session: AsyncSession, tenant_id: str, payload: DiningTableCreate
) -> FloorPlanTable:
    existing_code = await session.execute(
        select(FloorPlanTable.id).where(
            FloorPlanTable.tenant_id == tenant_id,
            FloorPlanTable.code == payload.code,
        )
    )
    if existing_code.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Table code already exists for tenant")

    if payload.zone_id:
        zone = await session.execute(
            select(FloorPlanZone.id).where(
                FloorPlanZone.id == payload.zone_id,
                FloorPlanZone.tenant_id == tenant_id,
            )
        )
        if zone.scalar_one_or_none() is None:
            raise HTTPException(status_code=404, detail="Zone not found for tenant")

    table = FloorPlanTable(
        tenant_id=tenant_id,
        zone_id=payload.zone_id,
        code=payload.code,
        qr_code=payload.qr_code,
        capacity=payload.capacity,
        status=payload.status,
        current_server_id=payload.current_server_id,
        parent_table_id=payload.parent_table_id,
        is_active=payload.is_active,
    )
    session.add(table)
    await session.commit()
    await session.refresh(table)
    return table

