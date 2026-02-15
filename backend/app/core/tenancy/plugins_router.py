"""
Legacy compatibility router.

This module used to expose an incomplete implementation that referenced an
undefined `repo`. To prevent accidental reactivation of broken endpoints, this
router now delegates to the canonical runtime router.
"""

from fastapi import APIRouter

from app.api.plugins_runtime import router as runtime_plugins_router


# Keep historical "/api/..." behavior when included directly on the FastAPI app.
router = APIRouter(prefix="/api")
router.include_router(runtime_plugins_router)
