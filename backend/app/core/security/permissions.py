from typing import Optional


def has_permission(user: Optional[dict], permission: str) -> bool:
    if not user:
        return False
    permissions = user.get("permissions", [])
    return permission in permissions
