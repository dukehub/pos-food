import enum
import uuid

from sqlalchemy import (
    Boolean, Column, DateTime, Enum, ForeignKey, Index, JSON, String,
    UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class TemplateType(str, enum.Enum):
    CUSTOMER_RECEIPT = "ticket_client"
    KITCHEN_TICKET = "ticket_cuisine"


class TicketTemplate(Base):
    __tablename__ = "ticket_template"
    __table_args__ = (
        Index("ix_ticket_template_tenant_name", "tenant_id", "name"),
        # Optionnel : éviter 2 templates avec le même nom pour le même tenant et type
        UniqueConstraint("tenant_id", "template_type", "name", name="uq_tt_tenant_type_name"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(120), nullable=False)

    template_type = Column(
        Enum(TemplateType, native_enum=False),
        nullable=False,
        default=TemplateType.KITCHEN_TICKET,
    )

    structure_json = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    # Optionnel : relation inverse
    assignments = relationship(
        "TicketTemplateAssignment",
        back_populates="template",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class TemplateScope(str, enum.Enum):
    KITCHEN = "kitchen"
    PRINTER = "printer"   # override par imprimante (optionnel)


class TicketTemplateAssignment(Base):
    __tablename__ = "ticket_template_assignment"
    __table_args__ = (
        # lookup rapide
        Index("ix_tta_tenant_scope_target", "tenant_id", "scope", "target_ref"),
        # 1 seul template par target (par type)
        UniqueConstraint(
            "tenant_id", "template_type", "scope", "target_ref",
            name="uq_tta_tenant_type_scope_target",
        ),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    template_id = Column(
        String(36),
        ForeignKey("ticket_template.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # On duplique template_type ici pour requêter sans join
    template_type = Column(
        Enum(TemplateType, native_enum=False),
        nullable=False,
    )

    scope = Column(
        Enum(TemplateScope, native_enum=False),
        nullable=False,
    )

    # IMPORTANT : référence “souple” compatible int/uuid
    # ex: "kitchen:12", "printer:550e8400-e29b-41d4-a716-446655440000"
    target_ref = Column(String(80), nullable=False)

    template = relationship("TicketTemplate", back_populates="assignments")
