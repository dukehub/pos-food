import enum
import uuid

from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, ForeignKey,
    UniqueConstraint, Index, Numeric, func, Table, Enum as SAEnum
)
from sqlalchemy.orm import relationship
from app.core.db.base import Base


def uuid_str():
    return str(uuid.uuid4())


# -----------------------
# PIVOT: Variant <-> Group
# -----------------------
product_modifier_groups = Table(
    "product_modifier_groups",
    Base.metadata,
    Column("product_id", String(36), ForeignKey("product.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", String(36), ForeignKey("modifier_group.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_pmg_product", "product_id"),
    Index("ix_pmg_group", "group_id"),
)

variant_modifier_groups = Table(
    "variant_modifier_groups",
    Base.metadata,
    Column("variant_id", String(36), ForeignKey("product_variant.id", ondelete="CASCADE"), primary_key=True),
    Column("group_id", String(36), ForeignKey("modifier_group.id", ondelete="CASCADE"), primary_key=True),
    Index("ix_vmg_variant", "variant_id"),
    Index("ix_vmg_group", "group_id"),
)


# --- Category ---

class Category(Base):
    __tablename__ = "category"
    __table_args__ = (
        UniqueConstraint("tenant_id", "slug", name="uq_category_tenant_slug"),
        Index("ix_category_tenant_parent", "tenant_id", "parent_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(50), nullable=False)
    slug = Column(String(50), nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    parent_id = Column(String(36), ForeignKey("category.id"), nullable=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    parent = relationship("Category", remote_side=[id], backref="children")
    products = relationship("Product", back_populates="category")

   

# --- Product ---

class Product(Base):
    __tablename__ = "product"
    __table_args__ = (
        UniqueConstraint("tenant_id", "slug", name="uq_product_tenant_slug"),
        Index("ix_product_tenant_category", "tenant_id", "category_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("category.id"), nullable=True)

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    slug = Column(String(100), nullable=False)
    sku = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    image_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    category = relationship("Category", back_populates="products")
    variants = relationship("ProductVariant", back_populates="product", cascade="all, delete-orphan")
     # ✅ groupes attachés à cette catégorie
    modifier_groups = relationship("ModifierGroup", secondary=product_modifier_groups, lazy="selectin")

# --- Product Variant ---

class ProductVariant(Base):
    __tablename__ = "product_variant"
    __table_args__ = (
        UniqueConstraint("tenant_id", "product_id", "variant_key", name="uq_pv_tenant_product_key"),
        Index("ix_pv_tenant_product", "tenant_id", "product_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    variant_key = Column(String(50), nullable=False)

    default_price = Column(Numeric(12, 2), default=0, nullable=False)
    sku = Column(String(50), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)
    image_url = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    product = relationship("Product", back_populates="variants")

    # ✅ groupes attachés à cette variante
    modifier_groups = relationship("ModifierGroup", secondary=variant_modifier_groups, lazy="selectin")


# --- Modifiers ---

class SelectionMode(str, enum.Enum):
    SINGLE = "single"
    MULTI = "multi"


class ModifierGroup(Base):
    __tablename__ = "modifier_group"
    __table_args__ = (
        UniqueConstraint("tenant_id", "code", name="uq_mg_tenant_code"),
        Index("ix_mg_tenant_order", "tenant_id", "sort_order"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)

    selection_mode = Column(SAEnum(SelectionMode), nullable=False, default=SelectionMode.SINGLE)
    min_select = Column(Integer, nullable=False, default=0)
    max_select = Column(Integer, nullable=False, default=1)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    items = relationship("ModifierItem", back_populates="group", cascade="all, delete-orphan")
    products = relationship("Product", secondary=product_modifier_groups, lazy="selectin")
    variants = relationship("ProductVariant", secondary=variant_modifier_groups, lazy="selectin")


class ModifierItem(Base):
    __tablename__ = "modifier_item"
    __table_args__ = (
        UniqueConstraint("tenant_id", "group_id", "code", name="uq_mi_tenant_group_code"),
        Index("ix_mi_tenant_group_order", "tenant_id", "group_id", "sort_order"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    group_id = Column(String(36), ForeignKey("modifier_group.id", ondelete="CASCADE"), nullable=False)

    code = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    price_delta = Column(Numeric(12, 2), default=0, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    group = relationship("ModifierGroup", back_populates="items")
