from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .models import Order, OrderLine
from .schemas import OrderCreate


async def list_orders(session: AsyncSession, tenant_id: str) -> list[Order]:
    rows = await session.execute(
        select(Order)
        .options(selectinload(Order.lines))
        .where(Order.tenant_id == tenant_id)
        .order_by(Order.created_at.desc())
    )
    return list(rows.scalars().all())


async def create_order(
    session: AsyncSession, tenant_id: str, payload: OrderCreate
) -> Order:
    order = Order(
        tenant_id=tenant_id,
        status=payload.status,
        note=payload.note,
        total_amount=Decimal("0.00"),
    )
    session.add(order)
    await session.flush()

    total = Decimal("0.00")
    for line in payload.lines:
        line_total = (line.unit_price * line.quantity).quantize(Decimal("0.01"))
        total += line_total

        session.add(
            OrderLine(
                tenant_id=tenant_id,
                order_id=order.id,
                product_id=line.product_id,
                variant_id=line.variant_id,
                name=line.name,
                quantity=line.quantity,
                unit_price=line.unit_price,
                line_total=line_total,
            )
        )

    order.total_amount = total.quantize(Decimal("0.01"))
    await session.commit()

    row = await session.execute(
        select(Order)
        .options(selectinload(Order.lines))
        .where(Order.id == order.id)
    )
    return row.scalar_one()

