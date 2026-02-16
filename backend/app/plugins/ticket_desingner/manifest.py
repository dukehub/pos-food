from app.core.plugins.manifest import PluginManifest

from .router import router
from .seed import seed

manifest = PluginManifest(
    key="ticket_desingner",
    name="Ticket Desingner",
    version="0.1.0",
    description="Ticket template designer for kitchen and customer prints.",
    router=router,
    requires=["floor_plan", "printer"],
    migrations_path="app.plugins.ticket_desingner.migrations",
    tables=["ticket_template", "ticket_template_assignment"],
    seed=seed,
    permissions=["ticket_desingner.read", "ticket_desingner.write"],
    ui_pages=[
        {"path": "/ticket_desingner/templates", "label": "Templates", "icon": "layout", "order": 100},
    ],
)
