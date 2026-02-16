import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SAEnum,
    Index,
    JSON,
    String,
    UniqueConstraint,
    func,
)

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class SettingScope(str, enum.Enum):
    TENANT = "tenant"   # global tenant (ton cas)
    DEVICE = "device"   # optionnel plus tard (ex: POS terminal)
    USER = "user"       # optionnel plus tard


class SettingValueType(str, enum.Enum):
    STRING = "string"
    NUMBER = "number"
    BOOLEAN = "boolean"
    OBJECT = "object"
    ARRAY = "array"
    ANY = "any"


class AppSetting(Base):
    __tablename__ = "app_setting"
    __table_args__ = (
        UniqueConstraint("tenant_id", "scope", "key", name="uq_app_setting_tenant_scope_key"),
        Index("ix_app_setting_tenant", "tenant_id"),
        Index("ix_app_setting_tenant_module", "tenant_id", "module"),
        Index("ix_app_setting_tenant_scope", "tenant_id", "scope"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)

    tenant_id = Column(String(36), nullable=False, index=True)

    # organisation
    scope = Column(SAEnum(SettingScope, native_enum=False), nullable=False, default=SettingScope.TENANT)
    module = Column(String(60), nullable=False, default="core")   # ex: "core", "pos", "ticket", "printer"

    # clé stable (ex: "app.currency", "ticket.footer_text")
    key = Column(String(120), nullable=False)

    # valeur (flexible)
    value_json = Column(JSON, nullable=False, default=dict)

    # optionnel: aide validation/affichage UI
    value_type = Column(SAEnum(SettingValueType, native_enum=False), nullable=False, default=SettingValueType.ANY)

    # optionnel: description pour UI admin
    description = Column(String(255), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
