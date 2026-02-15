import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    Numeric,
    String,
    func,
)

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class Customer(Base):
    __tablename__ = "customer"
    __table_args__ = (
        Index("ix_customer_tenant_name", "tenant_id", "name"),
        Index("ix_customer_tenant_phone", "tenant_id", "phone"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(120), nullable=False)
    phone = Column(String(32), nullable=True)
    email = Column(String(160), nullable=True)

    nif = Column(String(64), nullable=True)
    ai = Column(String(64), nullable=True)
    rc = Column(String(64), nullable=True)
    tax_id = Column(String(64), nullable=True)
    address = Column(String(255), nullable=True)

    current_balance = Column(Numeric(12, 2), nullable=False, default=0)
    credit_limit = Column(Numeric(12, 2), nullable=True)
    payment_due_days = Column(Integer, nullable=False, default=30)

    phone_whatsapp = Column(String(32), nullable=True)
    allow_notifications = Column(Boolean, nullable=False, default=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
