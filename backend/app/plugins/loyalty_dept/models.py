import enum
import uuid

from sqlalchemy import (
    Column,
    DateTime,
    Enum as SAEnum,
    Index,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class LedgerEntryType(str, enum.Enum):
    CHARGE = "charge"     # + dette
    PAYMENT = "payment"   # - paiement


class CustomerLedgerEntry(Base):
    __tablename__ = "customer_ledger"
    __table_args__ = (
        Index("ix_customer_ledger_tenant_customer_date", "tenant_id", "customer_id", "created_at"),
        Index("ix_customer_ledger_tenant_order", "tenant_id", "order_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    customer_id = Column(String(36), nullable=False, index=True)
    order_id = Column(String(36), nullable=True)  # string (FK optionnelle)

    entry_type = Column(SAEnum(LedgerEntryType), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)  # CHARGE:+  PAYMENT:-
    note = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)


class CustomerAccount(Base):
    """
    Cache du solde (optionnel). La source de vérité reste le ledger.
    """
    __tablename__ = "customer_account"
    __table_args__ = (
        UniqueConstraint("tenant_id", "customer_id", name="uq_customer_account_tenant_customer"),
        Index("ix_customer_account_tenant_customer", "tenant_id", "customer_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    customer_id = Column(String(36), nullable=False, index=True)

    balance = Column(Numeric(12, 2), nullable=False, default=0)  # >0 = dette, <0 = avance
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
