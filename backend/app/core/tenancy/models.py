from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db.base import Base, UUIDPrimaryKeyMixin

class Tenant(Base, UUIDPrimaryKeyMixin):
    __tablename__ = "tenants"

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    
    # Store settings
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    locale: Mapped[str] = mapped_column(String(10), default="en")

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
