import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, Index, String, UniqueConstraint, func

from app.core.db.base import Base


def uuid_str() -> str:
    return str(uuid.uuid4())


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    SERVER = "serveur"
    POS = "pos"


class StaffUser(Base):
    __tablename__ = "staff_user"
    __table_args__ = (
        UniqueConstraint("tenant_id", "username", name="uq_staff_user_tenant_username"),
        Index("ix_staff_user_tenant_role", "tenant_id", "role"),
    )

    id = Column(String(36), primary_key=True, default=uuid_str)
    tenant_id = Column(String(36), nullable=False, index=True)

    username = Column(String(80), nullable=False)
    full_name = Column(String(120), nullable=True)
    pin_code = Column(String(12), nullable=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.SERVER)
    language = Column(String(10), nullable=False, default="fr")
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)
