import uuid
from sqlalchemy import (
    Boolean, Column, DateTime, Integer, String, ForeignKey,
    UniqueConstraint, Index, Numeric, func
)
from sqlalchemy.orm import relationship
from app.core.db.base import Base

def uuid_str():
    return str(uuid.uuid4())


# --- Category ---

class Category(Base):
    __tablename__ = "category"
    __table_args__ = (
        UniqueConstraint("tenant_id", "slug", name="uq_category_tenant_slug"),
        Index("ix_category_tenant_parent", "tenant_id", "parent_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(50), nullable=False)   # fallback interne
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

    name = Column(String(100), nullable=False)          # fallback interne
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


# --- Product Variant ---

class ProductVariant(Base):
    __tablename__ = "product_variant"
    __table_args__ = (
        UniqueConstraint("tenant_id", "product_id", "variant_key", name="uq_product_variant_key"),
        Index("ix_product_variant_tenant_product", "tenant_id", "product_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("product.id"), nullable=False)

    name = Column(String(100), nullable=False)  # fallback interne
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
