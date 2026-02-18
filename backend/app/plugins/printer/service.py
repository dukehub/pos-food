from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import DevicePrinter
from .models import DevicePrinter
from .schemas import DevicePrinterCreate, DevicePrinterUpdate


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
    session.add(printer)
    await session.commit()
    await session.refresh(printer)
    return printer


async def update_printer(
    session: AsyncSession, tenant_id: str, printer_id: str, payload: DevicePrinterCreate
) -> DevicePrinter:
    printer = await session.get(DevicePrinter, printer_id)
    if not printer or printer.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Printer not found")

    if payload.name and payload.name != printer.name:
        existing = await session.execute(
            select(DevicePrinter.id).where(
                DevicePrinter.tenant_id == tenant_id,
                DevicePrinter.name == payload.name,
            )
        )
        if existing.scalar_one_or_none() is not None:
             raise HTTPException(status_code=409, detail="Printer name already exists for tenant")

    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(printer, key, value)

    await session.commit()
    await session.refresh(printer)
    return printer


async def delete_printer(session: AsyncSession, tenant_id: str, printer_id: str):
    printer = await session.get(DevicePrinter, printer_id)
    if not printer or printer.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Printer not found")

    await session.delete(printer)
    await session.commit()

