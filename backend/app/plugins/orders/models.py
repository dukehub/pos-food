import uuid

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        Index("ix_orders_tenant_created", "tenant_id", "created_at"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    status = Column(String(30), nullable=False, default="draft")
    note = Column(String(255), nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    lines = relationship(
        "OrderLine",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class OrderLine(Base):
    __tablename__ = "order_line"
    __table_args__ = (
        Index("ix_order_line_tenant_order", "tenant_id", "order_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    order_id = Column(String(36), ForeignKey("orders.id"), nullable=False)

    product_id = Column(String(36), nullable=True)
    variant_id = Column(String(36), nullable=True)

    name = Column(String(120), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(12, 2), nullable=False, default=0)
    line_total = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="lines")

