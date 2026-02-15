from contextvars import ContextVar
from typing import Optional

_current_tenant_id: ContextVar[Optional[str]] = ContextVar("tenant_id", default=None)


def set_tenant_id(tenant_id: Optional[str]) -> object:
    return _current_tenant_id.set(tenant_id)


def reset_tenant_id(token: object) -> None:
    _current_tenant_id.reset(token)


def get_tenant_id() -> Optional[str]:
    return _current_tenant_id.get()
