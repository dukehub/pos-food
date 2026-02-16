import uuid

from sqlalchemy import (
    Boolean,
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
        Index("ix_orders_tenant_status_created", "tenant_id", "status", "created_at"),
        Index("ix_orders_tenant_customer", "tenant_id", "customer_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    # client fidèle (nullable pour vente comptoir)
    customer_id = Column(String(36), nullable=True)  # FK("customer.id") si tu veux couplage

    status = Column(String(30), nullable=False, default="draft")  # draft/confirmed/closed/cancelled
    note = Column(String(255), nullable=True)

    total_amount = Column(Numeric(12, 2), nullable=False, default=0)

    # caches utiles POS
    amount_paid = Column(Numeric(12, 2), nullable=False, default=0)
    amount_due = Column(Numeric(12, 2), nullable=False, default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    lines = relationship(
        "OrderLine",
        back_populates="order",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )


class OrderLine(Base):
    __tablename__ = "order_line"
    __table_args__ = (
        Index("ix_order_line_tenant_order", "tenant_id", "order_id"),
        Index("ix_order_line_tenant_product", "tenant_id", "product_id"),
        Index("ix_order_line_tenant_variant", "tenant_id", "variant_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    order_id = Column(
        String(36),
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ✅ Recommandé: garder les snapshots, et FK optionnelles (selon ta stratégie)
    product_id = Column(String(36), nullable=True)  # ou ForeignKey("product.id", ondelete="SET NULL")
    variant_id = Column(String(36), nullable=True)  # ou ForeignKey("product_variant.id", ondelete="SET NULL")

    name_snapshot = Column(String(160), nullable=False)  # ex: "Chakchouka - Poulet"
    note = Column(String(255), nullable=True)            # note cuisine

    quantity = Column(Integer, nullable=False, default=1)

    unit_price = Column(Numeric(12, 2), nullable=False, default=0)      # prix de base (variant)
    modifiers_total = Column(Numeric(12, 2), nullable=False, default=0) # suppléments
    line_total = Column(Numeric(12, 2), nullable=False, default=0)      # total ligne

    sort_order = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    order = relationship("Order", back_populates="lines")

    # ✅ si tu implémentes OrderLineModifier (extras), ajoute:
    modifiers = relationship("OrderLineModifier", back_populates="line",cascade="all, delete-orphan", passive_deletes=True, lazy="selectin")

class OrderLineModifier(Base):
    __tablename__ = "order_line_modifier"
    __table_args__ = (
        Index("ix_olm_tenant_line", "tenant_id", "line_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    line_id = Column(String(36), ForeignKey("order_line.id", ondelete="CASCADE"), nullable=False)

    group_name_snapshot = Column(String(100), nullable=False)  # "Viande"
    item_name_snapshot = Column(String(100), nullable=False)   # "Poulet"
    price_delta = Column(Numeric(12, 2), nullable=False, default=0)

    line = relationship("OrderLine", back_populates="modifiers")
