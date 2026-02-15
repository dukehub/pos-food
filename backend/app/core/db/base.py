import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    pass

def uuid_str() -> str:
    return str(uuid.uuid4())

class UUIDPrimaryKeyMixin:
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=uuid_str)

class TenantMixin:
    tenant_id: Mapped[str] = mapped_column(String(36), index=True, nullable=False)