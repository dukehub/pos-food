from typing import Optional

from fastapi import Header


async def get_current_user(
    x_user_id: Optional[str] = Header(default=None, alias="X-User-Id"),
    x_user_permissions: Optional[str] = Header(default=None, alias="X-User-Permissions"),
) -> Optional[dict]:
    if not x_user_id:
        return None

    permissions = []
    if x_user_permissions:
        permissions = [p.strip() for p in x_user_permissions.split(",") if p.strip()]

    return {"id": x_user_id, "permissions": permissions}
