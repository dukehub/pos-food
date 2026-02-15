from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Invoice
from .schemas import InvoiceCreate


async def list_invoices(session: AsyncSession, tenant_id: str) -> list[Invoice]:
    rows = await session.execute(
        select(Invoice)
        .where(Invoice.tenant_id == tenant_id)
        .order_by(Invoice.created_at.desc())
    )
    return list(rows.scalars().all())


async def create_invoice(
    session: AsyncSession, tenant_id: str, payload: InvoiceCreate
) -> Invoice:
    existing = await session.execute(
        select(Invoice.id).where(
            Invoice.tenant_id == tenant_id,
            Invoice.number == payload.number,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Invoice number already exists for tenant")

    invoice = Invoice(
        tenant_id=tenant_id,
        number=payload.number,
        customer_id=payload.customer_id,
        customer_name=payload.customer_name,
        customer_tax_id=payload.customer_tax_id,
        customer_address=payload.customer_address,
        total_amount=payload.total_amount,
    )
    session.add(invoice)
    await session.commit()
    await session.refresh(invoice)
    return invoice
