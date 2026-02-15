import uuid

from sqlalchemy import Boolean, Column, DateTime, String, UniqueConstraint, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class RestaurantConfig(Base):
    __tablename__ = "restaurant_config"
    __table_args__ = (
        UniqueConstraint("tenant_id", name="uq_restaurant_config_tenant"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    name = Column(String(120), nullable=False, default="")
    slug = Column(String(120), nullable=False, default="")
    currency = Column(String(16), nullable=False, default="USD")
    locale = Column(String(16), nullable=False, default="fr")

    address = Column(String(255), nullable=False, default="")
    phone = Column(String(32), nullable=False, default="")
    email = Column(String(160), nullable=False, default="")

    tax_nif = Column(String(64), nullable=False, default="")
    tax_rc = Column(String(64), nullable=False, default="")
    tax_ai = Column(String(64), nullable=False, default="")

    logo_url = Column(String(255), nullable=False, default="")
    background_image_url = Column(String(255), nullable=False, default="")
    background_image_secondary_url = Column(String(255), nullable=False, default="")

    location_label = Column(String(255), nullable=False, default="")
    city = Column(String(120), nullable=False, default="")
    country = Column(String(120), nullable=False, default="")
    postal_code = Column(String(32), nullable=False, default="")
    latitude = Column(String(32), nullable=False, default="")
    longitude = Column(String(32), nullable=False, default="")

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

