from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import TicketTemplate
from .schemas import TicketTemplateCreate


async def list_templates(session: AsyncSession, tenant_id: str) -> list[TicketTemplate]:
    rows = await session.execute(
        select(TicketTemplate)
        .where(TicketTemplate.tenant_id == tenant_id)
        .order_by(TicketTemplate.name.asc())
    )
    return list(rows.scalars().all())


async def create_template(
    session: AsyncSession, tenant_id: str, payload: TicketTemplateCreate
) -> TicketTemplate:
    existing = await session.execute(
        select(TicketTemplate.id).where(
            TicketTemplate.tenant_id == tenant_id,
            TicketTemplate.name == payload.name,
        )
    )
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=409, detail="Template name already exists for tenant")

    template = TicketTemplate(
        tenant_id=tenant_id,
        name=payload.name,
        template_type=payload.template_type,
        structure_json=payload.structure_json,
        is_active=payload.is_active,
    )
    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template
