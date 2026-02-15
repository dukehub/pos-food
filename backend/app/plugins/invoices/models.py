import uuid

from sqlalchemy import Column, DateTime, Index, Numeric, String, UniqueConstraint, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class Invoice(Base):
    __tablename__ = "invoice"
    __table_args__ = (
        UniqueConstraint("tenant_id", "number", name="uq_invoice_tenant_number"),
        Index("ix_invoice_tenant_created", "tenant_id", "created_at"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    number = Column(String(50), nullable=False)
    customer_id = Column(String(36), nullable=True)
    customer_name = Column(String(120), nullable=True)
    customer_tax_id = Column(String(64), nullable=True)
    customer_address = Column(String(255), nullable=True)

    total_amount = Column(Numeric(12, 2), nullable=False, default=0)
    created_at = Column(DateTime, default=func.now(), nullable=False)
