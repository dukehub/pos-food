import uuid

from sqlalchemy import Boolean, Column, DateTime, Numeric, String, UniqueConstraint, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class RestaurantConfig(Base):
    __tablename__ = "restaurant_config"
    __table_args__ = (
        UniqueConstraint("tenant_id", name="uq_restaurant_config_tenant"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False)  # l'unique constraint suffit

    name = Column(String(120), nullable=False)
    slug = Column(String(120), nullable=False)

    currency = Column(String(16), nullable=False, default="DZD")
    locale = Column(String(16), nullable=False, default="fr-DZ")

    address = Column(String(255), nullable=True)
    phone = Column(String(32), nullable=True)
    email = Column(String(160), nullable=True)

    tax_nif = Column(String(64), nullable=True)
    tax_rc = Column(String(64), nullable=True)
    tax_ai = Column(String(64), nullable=True)

    logo_url = Column(String(255), nullable=True)
    background_image_url = Column(String(255), nullable=True)
    background_image_secondary_url = Column(String(255), nullable=True)

    location_label = Column(String(255), nullable=True)
    city = Column(String(120), nullable=True)
    country = Column(String(120), nullable=True)
    postal_code = Column(String(32), nullable=True)

    latitude = Column(Numeric(10, 7), nullable=True)
    longitude = Column(Numeric(10, 7), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


