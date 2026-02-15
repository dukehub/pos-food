import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, JSON, String, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class TemplateType(str, enum.Enum):
    CUSTOMER_RECEIPT = "ticket_client"
    KITCHEN_TICKET = "ticket_cuisine"
    INVOICE = "facture_a4"


class TicketTemplate(Base):
    __tablename__ = "ticket_template"
    __table_args__ = (
        Index("ix_ticket_template_tenant_name", "tenant_id", "name"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(120), nullable=False)
    template_type = Column(Enum(TemplateType), nullable=False, default=TemplateType.KITCHEN_TICKET)
    structure_json = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
