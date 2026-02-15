import uuid
from sqlalchemy import (
    Column, String, ForeignKey, UniqueConstraint, Index, Text
)
from sqlalchemy.orm import relationship
from app.core.db.base import Base

def uuid_str():
    return str(uuid.uuid4())


# --- Category Translation ---

class CategoryTranslation(Base):
    __tablename__ = "category_translation"
    __table_args__ = (
        UniqueConstraint("tenant_id", "category_id", "locale", name="uq_category_tr"),
        Index("ix_category_tr_tenant_locale", "tenant_id", "locale"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    category_id = Column(String(36), ForeignKey("category.id", ondelete="CASCADE"), nullable=False)

    locale = Column(String(16), nullable=False)  # ar-DZ / fr-DZ
    name = Column(String(50), nullable=False)

    category = relationship("Category")


# --- Product Translation ---

class ProductTranslation(Base):
    __tablename__ = "product_translation"
    __table_args__ = (
        UniqueConstraint("tenant_id", "product_id", "locale", name="uq_product_tr"),
        Index("ix_product_tr_tenant_locale", "tenant_id", "locale"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    locale = Column(String(16), nullable=False)
    name = Column(String(100), nullable=False)
    name_norm = Column(Text, nullable=False)   # important pour recherche
    description = Column(String(255), nullable=True)

    product = relationship("Product")


# --- Variant Translation ---

class ProductVariantTranslation(Base):
    __tablename__ = "product_variant_translation"
    __table_args__ = (
        UniqueConstraint("tenant_id", "variant_id", "locale", name="uq_product_variant_tr"),
        Index("ix_variant_tr_tenant_locale", "tenant_id", "locale"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    variant_id = Column(String(36), ForeignKey("product_variant.id", ondelete="CASCADE"), nullable=False)

    locale = Column(String(16), nullable=False)
    name = Column(String(100), nullable=False)
    name_norm = Column(Text, nullable=False)
    description = Column(String(255), nullable=True)

    variant = relationship("ProductVariant")


# --- Product Alias (synonymes / darija search) ---

class ProductAlias(Base):
    __tablename__ = "product_alias"
    __table_args__ = (
        UniqueConstraint("tenant_id", "product_id", "locale", "alias_norm", name="uq_product_alias_norm"),
        Index("ix_product_alias_tenant_locale", "tenant_id", "locale"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)
    product_id = Column(String(36), ForeignKey("product.id", ondelete="CASCADE"), nullable=False)

    locale = Column(String(16), nullable=False)
    alias = Column(String(100), nullable=False)
    alias_norm = Column(Text, nullable=False)

    product = relationship("Product")
