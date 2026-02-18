from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Customer
from .models import Customer
from .schemas import CustomerCreate, CustomerUpdate


async def list_customers(session: AsyncSession, tenant_id: str) -> list[Customer]:
    rows = await session.execute(
        select(Customer)
        .where(Customer.tenant_id == tenant_id)
        .order_by(Customer.name.asc())
    )
    return list(rows.scalars().all())


async def create_customer(
    session: AsyncSession, tenant_id: str, payload: CustomerCreate
) -> Customer:
    if payload.phone:
        existing_phone = await session.execute(
            select(Customer.id).where(
                Customer.tenant_id == tenant_id,
                Customer.phone == payload.phone,
            )
        )
        if existing_phone.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail="Phone already exists for tenant")

    customer = Customer(
        tenant_id=tenant_id,
        name=payload.name,
        phone=payload.phone,
        email=payload.email,
        nif=payload.nif,
        ai=payload.ai,
        rc=payload.rc,
        tax_id=payload.tax_id,
        address=payload.address,
        credit_limit=payload.credit_limit,
        payment_due_days=payload.payment_due_days,
        phone_whatsapp=payload.phone_whatsapp,
        allow_notifications=payload.allow_notifications,
        is_active=payload.is_active,
    )
    session.add(customer)
    await session.commit()
    await session.refresh(customer)
    return customer


async def update_customer(
    session: AsyncSession, tenant_id: str, customer_id: str, payload: CustomerCreate
) -> Customer:  # Using Create/Update schema dynamically or just payload
    customer = await session.get(Customer, customer_id)
    if not customer or customer.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Check phone uniqueness if changing
    if payload.phone is not None and payload.phone != customer.phone:
        existing_phone = await session.execute(
            select(Customer.id).where(
                Customer.tenant_id == tenant_id,
                Customer.phone == payload.phone,
            )
        )
        if existing_phone.scalar_one_or_none() is not None:
            raise HTTPException(status_code=409, detail="Phone already exists for tenant")

    # Update fields
    # Note: payload is CustomerUpdate in router, but typed as CustomerCreate here? 
    # Let's trust the router to pass the right schema or compatible object.
    # In router I will type it as CustomerUpdate.
    
    data = payload.model_dump(exclude_unset=True)
    for key, value in data.items():
        setattr(customer, key, value)

    await session.commit()
    await session.refresh(customer)
    return customer


async def delete_customer(session: AsyncSession, tenant_id: str, customer_id: str):
    customer = await session.get(Customer, customer_id)
    if not customer or customer.tenant_id != tenant_id:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    await session.delete(customer)
    await session.commit()
