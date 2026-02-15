from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db.base import Base


class Plugin(Base):
    __tablename__ = "plugins"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(500), default="")
    version: Mapped[str] = mapped_column(String(50), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    tenant_links = relationship("TenantPlugin", back_populates="plugin")


class TenantPlugin(Base):
    __tablename__ = "tenant_plugins"
    __table_args__ = (UniqueConstraint("tenant_id", "plugin_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(120), index=True)
    plugin_id: Mapped[int] = mapped_column(ForeignKey("plugins.id"))
    is_enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    # NEW
    installed_version: Mapped[str | None] = mapped_column(String(50), nullable=True)
    installed_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    plugin = relationship("Plugin", back_populates="tenant_links")


class Permission(Base):
    __tablename__ = "permissions"
    __table_args__ = (UniqueConstraint("tenant_id", "code", name="uq_permissions_tenant_code"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(120), index=True)
    code: Mapped[str] = mapped_column(String(120), index=True)
    label: Mapped[str] = mapped_column(String(200))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    # plugin = relationship("Plugin", back_populates="tenant_links")
