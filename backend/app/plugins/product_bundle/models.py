import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class ProductBundleItem(Base):
    __tablename__ = "product_bundle_item"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "parent_product_id",
            "child_product_id",
            name="uq_product_bundle_item_pair",
        ),
        Index("ix_product_bundle_item_tenant_parent", "tenant_id", "parent_product_id"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    parent_product_id = Column(String(36), nullable=False)
    child_product_id = Column(String(36), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
