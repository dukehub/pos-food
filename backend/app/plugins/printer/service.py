from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DevicePrinter
from .schemas import DevicePrinterCreate


async def list_printers(session: AsyncSession, tenant_id: str) -> list[DevicePrinter]:
    rows = await session.execute(
        select(DevicePrinter)
        .where(DevicePrinter.tenant_id == tenant_id)
        .order_by(DevicePrinter.name.asc())
    )
    return list(rows.scalars().all())


async def create_printer(
    session: AsyncSession, tenant_id: str, payload: DevicePrinterCreate
) -> DevicePrinter:
    existing = await session.execute(
        select(DevicePrinter.id).where(
            DevicePrinter.tenant_id == tenant_id,
            DevicePrinter.name == payload.name,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Printer name already exists for tenant")

    printer = DevicePrinter(
        tenant_id=tenant_id,
        name=payload.name,
        driver_type=payload.driver_type,
        system_printer_name=payload.system_printer_name,
        ip_address=payload.ip_address,
        port=payload.port,
        paper_width=payload.paper_width,
        is_active=payload.is_active,
    )
    session.add(printer)
    await session.commit()
    await session.refresh(printer)
    return printer

