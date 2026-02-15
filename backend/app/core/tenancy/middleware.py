from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.config.settings import settings
from app.core.tenancy.context import reset_tenant_id, set_tenant_id


class TenancyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tenant_id = request.headers.get(settings.tenant_header) or "public"
        token = set_tenant_id(tenant_id)
        try:
            response = await call_next(request)
        finally:
            reset_tenant_id(token)
        return response
