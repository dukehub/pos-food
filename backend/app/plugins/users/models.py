import enum
import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Index,
    String,
    UniqueConstraint,
    func,
)

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    WAITER = "waiter"
    CASHIER = "cashier"


class StaffUser(Base):
    __tablename__ = "staff_user"
    __table_args__ = (
        UniqueConstraint("tenant_id", "username", name="uq_staff_user_tenant_username"),
        Index("ix_staff_user_tenant_role", "tenant_id", "role"),
        Index("ix_staff_user_tenant_active", "tenant_id", "is_active"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    username = Column(String(80), nullable=False)
    full_name = Column(String(120), nullable=True)

    # ✅ contient toujours un hash (mot de passe normal OU PIN)
    password_hash = Column(String(255), nullable=False)

    role = Column(Enum(UserRole, native_enum=False), nullable=False, default=UserRole.WAITER)
    language = Column(String(16), nullable=False, default="fr-DZ")
    avatar_url = Column(String(255), nullable=True)

    is_active = Column(Boolean, nullable=False, default=True)
    last_login_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
