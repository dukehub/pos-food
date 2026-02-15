import os
import importlib
import pytest
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def client(tmp_path_factory):
    # DB sqlite de test
    tmpdir = tmp_path_factory.mktemp("db")
    db_path = tmpdir / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path}"

    # Reload settings/session pour recréer engine avec DATABASE_URL
    import app.core.config.settings as settings_mod
    importlib.reload(settings_mod)

    import app.core.db.session as session_mod
    importlib.reload(session_mod)

    # Reload runtime pour qu'il utilise le nouvel engine (sync_database)
    import app.core.plugins.runtime as plugins_runtime_core
    importlib.reload(plugins_runtime_core)

    # Reload api routers pour qu'ils utilisent le nouveau get_session
    import app.api.plugins_runtime as plugins_runtime_api
    importlib.reload(plugins_runtime_api)
    
    # Also reload main api router if needed, or ensuring dependencies propagates
    # import app.api.router as api_router_mod
    # importlib.reload(api_router_mod)

    # Recharge main (important car app dépend des modules au import)
    import app.main as main_mod
    importlib.reload(main_mod)

    with TestClient(main_mod.app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_list_plugins(client):
    r = client.get("/api/tenants/clientA/plugins")
    assert r.status_code == 200
    data = r.json()
    assert "plugins" in data
    assert isinstance(data["plugins"], list)
    # au moins un plugin chargé
    assert len(data["plugins"]) >= 1


def test_no_double_tenants_prefix(client):
    # Cette route doit exister (pas /api/tenants/tenants/..)
    r = client.get("/api/tenants/clientA/plugins")
    assert r.status_code == 200


def test_enable_plugin_triggers_install(client):
    # adapte la key selon tes plugins réels
    plugin_key = "catalog_product"

    r = client.post(f"/api/tenants/clientA/plugins/{plugin_key}:enable")
    assert r.status_code == 200, r.text
    data = r.json()

    # Doit être enabled
    assert data["enabled"] is True

    # Si lifecycle OK : installed_version doit être retournée
    assert "to_version" in data

def test_plugin_migrations_created_tables(client):
    plugin_key = "catalog_product"
    r = client.post(f"/api/tenants/clientA/plugins/{plugin_key}:install")
    assert r.status_code == 200, r.text

    # On utilise l'event loop via la session async (option simple: appel direct engine sync)
    # Si tu exposes un engine sync quelque part c'est plus simple.
    # Sinon, test minimal: on appelle une route du plugin qui dépend de DB (si tu en as).

def test_disable_blocks_plugin_routes(client):
    plugin_key = "catalog_product"
    tenant_id = "clientA"
    headers = {"X-Tenant-Id": tenant_id}

    client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    
    # 1. Enabled -> 200 OK
    r = client.get(f"/api/plugins/{plugin_key}/health", headers=headers) 
    assert r.status_code == 200
    assert r.json()["service"] == "catalog_product"

    # 2. Disabled -> 404 (due to Dependency check raising 404)
    client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:disable")
    
    r2 = client.get(f"/api/plugins/{plugin_key}/health", headers=headers)
    assert r2.status_code == 404


def test_plugin_route_prefix_convention(client):
    tenant_id = "clientA"
    headers = {"X-Tenant-Id": tenant_id}
    plugin_key = "catalog_product"

    client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")

    new_route = client.get(f"/api/plugins/{plugin_key}/health", headers=headers)
    assert new_route.status_code == 200

    old_route = client.get(f"/api/{plugin_key}/health", headers=headers)
    assert old_route.status_code == 404


def test_plugin_dependency_enforced(client):
    tenant_id = "client-dependency-check"
    dependent = "catalog_product_i18n"

    r = client.post(f"/api/tenants/{tenant_id}/plugins/{dependent}:enable")
    assert r.status_code == 409
    body = r.json()
    assert body["detail"]["error"] == "missing_dependencies"
    assert "catalog_product" in body["detail"]["missing"]


def test_disable_dependency_blocked_when_dependents_enabled(client):
    tenant_id = "client-disable-dependency"
    base = "catalog_product"
    dependent = "catalog_product_i18n"

    r_base = client.post(f"/api/tenants/{tenant_id}/plugins/{base}:enable")
    assert r_base.status_code == 200, r_base.text

    r_dependent = client.post(f"/api/tenants/{tenant_id}/plugins/{dependent}:enable")
    assert r_dependent.status_code == 200, r_dependent.text

    r_disable_base = client.post(f"/api/tenants/{tenant_id}/plugins/{base}:disable")
    assert r_disable_base.status_code == 409, r_disable_base.text
    body = r_disable_base.json()
    assert body["detail"]["error"] == "plugin_required_by_enabled_plugins"
    assert dependent in body["detail"]["required_by"]


def test_ui_menu_exposes_enabled_plugin_pages(client):
    tenant_id = "clientA"
    plugin_key = "catalog_product"

    client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    r = client.get(f"/api/tenants/{tenant_id}/ui/menu")

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["tenant_id"] == tenant_id
    assert any(page["plugin"] == plugin_key for page in body["pages"])


def test_floor_plan_plugin_enable_and_health(client):
    tenant_id = "tenant-floor-base"
    plugin_key = "floor_plan"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    assert r_enable.status_code == 200, r_enable.text

    r_health = client.get(f"/api/plugins/{plugin_key}/health", headers=headers)
    assert r_health.status_code == 200, r_health.text
    assert r_health.json()["service"] == "floor_plan"


def test_floor_plan_create_zone_and_table(client):
    tenant_id = "tenant-floor-crud"
    headers = {"X-Tenant-Id": tenant_id}
    plugin_key = "floor_plan"

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    assert r_enable.status_code == 200, r_enable.text

    zone_payload = {"name": "Main Room", "display_order": 1, "is_active": True}
    r_zone = client.post("/api/plugins/floor_plan/zones", json=zone_payload, headers=headers)
    assert r_zone.status_code == 201, r_zone.text
    zone = r_zone.json()

    table_payload = {
        "code": "T01",
        "zone_id": zone["id"],
        "capacity": 4,
        "status": "FREE",
        "is_active": True,
    }
    r_table = client.post(
        "/api/plugins/floor_plan/tables", json=table_payload, headers=headers
    )
    assert r_table.status_code == 201, r_table.text
    table = r_table.json()
    assert table["code"] == "T01"
    assert table["zone_id"] == zone["id"]

    r_tables = client.get("/api/plugins/floor_plan/tables", headers=headers)
    assert r_tables.status_code == 200, r_tables.text
    items = r_tables.json()
    assert any(item["id"] == table["id"] for item in items)


def test_orders_dependency_on_catalog_product(client):
    tenant_id = "tenant-orders-dep"
    plugin_key = "orders"

    r = client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["detail"]["error"] == "missing_dependencies"
    assert "catalog_product" in body["detail"]["missing"]


def test_orders_create_and_list(client):
    tenant_id = "tenant-orders-ok"
    headers = {"X-Tenant-Id": tenant_id}

    # Required dependency first
    r_catalog = client.post(f"/api/tenants/{tenant_id}/plugins/catalog_product:enable")
    assert r_catalog.status_code == 200, r_catalog.text

    r_orders = client.post(f"/api/tenants/{tenant_id}/plugins/orders:enable")
    assert r_orders.status_code == 200, r_orders.text

    payload = {
        "status": "draft",
        "note": "Test order",
        "lines": [
            {"name": "Pizza Margherita", "quantity": 2, "unit_price": "12.50"},
            {"name": "Coca Cola", "quantity": 1, "unit_price": "3.00"},
        ],
    }
    r_create = client.post("/api/plugins/orders/orders", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["total_amount"] == "28.00"
    assert len(created["lines"]) == 2

    r_list = client.get("/api/plugins/orders/orders", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert len(items) >= 1
    assert any(item["id"] == created["id"] for item in items)


def test_customers_create_and_list(client):
    tenant_id = "tenant-customers-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/customers:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "name": "John Doe",
        "phone": "+213555000111",
        "email": "john@example.com",
        "allow_notifications": True,
    }
    r_create = client.post(
        "/api/plugins/customers/customers", json=payload, headers=headers
    )
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["name"] == payload["name"]
    assert created["phone"] == payload["phone"]

    r_list = client.get("/api/plugins/customers/customers", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_devices_create_and_list(client):
    tenant_id = "tenant-devices-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/devices:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "name": "Main Device Terminal",
        "device_type": "terminal",
        "identifier": "TERM-01",
        "location": "Front Counter",
        "ip_address": "192.168.1.200",
        "is_active": True,
    }
    r_create = client.post("/api/plugins/devices/devices", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["name"] == payload["name"]
    assert created["device_type"] == payload["device_type"]

    r_list = client.get("/api/plugins/devices/devices", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_printer_depends_on_devices(client):
    tenant_id = "tenant-printer-dep"
    r = client.post(f"/api/tenants/{tenant_id}/plugins/printer:enable")
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["detail"]["error"] == "missing_dependencies"
    assert "devices" in body["detail"]["missing"]


def test_printer_create_and_list(client):
    tenant_id = "tenant-printer-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_devices = client.post(f"/api/tenants/{tenant_id}/plugins/devices:enable")
    assert r_devices.status_code == 200, r_devices.text

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/printer:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "name": "Kitchen Printer 1",
        "driver_type": "network",
        "ip_address": "192.168.1.210",
        "port": 9100,
        "paper_width": 80,
        "is_active": True,
    }
    r_create = client.post("/api/plugins/printer/printers", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["name"] == payload["name"]
    assert created["driver_type"] == payload["driver_type"]

    r_list = client.get("/api/plugins/printer/printers", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_kds_create_and_list(client):
    tenant_id = "tenant-kds-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_devices = client.post(f"/api/tenants/{tenant_id}/plugins/devices:enable")
    assert r_devices.status_code == 200, r_devices.text

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/kds:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "name": "Main Kitchen Display",
        "ip_address": "192.168.1.220",
        "port": 3010,
        "location": "Cuisine chaude",
        "is_active": True,
    }
    r_create = client.post("/api/plugins/kds/kds", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["name"] == payload["name"]
    assert created["port"] == payload["port"]

    r_list = client.get("/api/plugins/kds/kds", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_users_create_and_list(client):
    tenant_id = "tenant-users-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/users:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "username": "server01",
        "full_name": "Server One",
        "role": "serveur",
        "language": "fr",
        "is_active": True,
    }
    r_create = client.post("/api/plugins/users/users", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["username"] == payload["username"]
    assert created["role"] == payload["role"]

    r_list = client.get("/api/plugins/users/users", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_invoices_dependency_on_customers(client):
    tenant_id = "tenant-invoices-dep"
    plugin_key = "invoices"

    r = client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["detail"]["error"] == "missing_dependencies"
    assert "customers" in body["detail"]["missing"]


def test_invoices_create_and_list(client):
    tenant_id = "tenant-invoices-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_customers = client.post(f"/api/tenants/{tenant_id}/plugins/customers:enable")
    assert r_customers.status_code == 200, r_customers.text

    r_invoices = client.post(f"/api/tenants/{tenant_id}/plugins/invoices:enable")
    assert r_invoices.status_code == 200, r_invoices.text

    payload = {
        "number": "INV-2026-0001",
        "customer_name": "John Doe",
        "customer_tax_id": "NIF-123",
        "customer_address": "Algiers",
        "total_amount": "125.50",
    }
    r_create = client.post("/api/plugins/invoices/invoices", json=payload, headers=headers)
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["number"] == payload["number"]
    assert created["total_amount"] == payload["total_amount"]

    r_list = client.get("/api/plugins/invoices/invoices", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_ticket_desingner_create_and_list(client):
    tenant_id = "tenant-ticket-designer-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/ticket_desingner:enable")
    assert r_enable.status_code == 200, r_enable.text

    payload = {
        "name": "Kitchen Default",
        "template_type": "ticket_cuisine",
        "structure_json": {"sections": ["header", "items", "footer"]},
        "is_active": True,
    }
    r_create = client.post(
        "/api/plugins/ticket_desingner/templates", json=payload, headers=headers
    )
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["name"] == payload["name"]
    assert created["template_type"] == payload["template_type"]

    r_list = client.get("/api/plugins/ticket_desingner/templates", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_product_bundle_dependency_on_catalog_product(client):
    tenant_id = "tenant-product-bundle-dep"
    plugin_key = "product_bundle"

    r = client.post(f"/api/tenants/{tenant_id}/plugins/{plugin_key}:enable")
    assert r.status_code == 409, r.text
    body = r.json()
    assert body["detail"]["error"] == "missing_dependencies"
    assert "catalog_product" in body["detail"]["missing"]


def test_product_bundle_create_and_list(client):
    tenant_id = "tenant-product-bundle-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_catalog = client.post(f"/api/tenants/{tenant_id}/plugins/catalog_product:enable")
    assert r_catalog.status_code == 200, r_catalog.text

    r_bundle = client.post(f"/api/tenants/{tenant_id}/plugins/product_bundle:enable")
    assert r_bundle.status_code == 200, r_bundle.text

    payload = {
        "parent_product_id": "prod-parent-001",
        "child_product_id": "prod-child-001",
        "quantity": 2,
        "is_active": True,
    }
    r_create = client.post(
        "/api/plugins/product_bundle/bundles", json=payload, headers=headers
    )
    assert r_create.status_code == 201, r_create.text
    created = r_create.json()
    assert created["parent_product_id"] == payload["parent_product_id"]
    assert created["child_product_id"] == payload["child_product_id"]
    assert created["quantity"] == payload["quantity"]

    r_list = client.get("/api/plugins/product_bundle/bundles", headers=headers)
    assert r_list.status_code == 200, r_list.text
    items = r_list.json()
    assert any(item["id"] == created["id"] for item in items)


def test_config_get_and_update_restaurant_info(client):
    tenant_id = "tenant-config-ok"
    headers = {"X-Tenant-Id": tenant_id}

    r_enable = client.post(f"/api/tenants/{tenant_id}/plugins/config:enable")
    assert r_enable.status_code == 200, r_enable.text

    r_get_initial = client.get("/api/plugins/config/restaurant", headers=headers)
    assert r_get_initial.status_code == 200, r_get_initial.text
    initial = r_get_initial.json()
    assert initial["tenant_id"] == tenant_id
    assert initial["currency"] == "USD"
    assert initial["locale"] == "fr"

    payload = {
        "name": "Le Bistrot Central",
        "slug": "le-bistrot-central",
        "currency": "DZD",
        "locale": "fr",
        "address": "Rue Didouche Mourad, Alger",
        "phone": "+213555123456",
        "email": "contact@bistrot.dz",
        "tax_nif": "NIF-2026-001",
        "tax_rc": "RC-2026-002",
        "tax_ai": "AI-2026-003",
        "logo_url": "https://cdn.example.com/logo.png",
        "background_image_url": "https://cdn.example.com/bg-main.jpg",
        "background_image_secondary_url": "https://cdn.example.com/bg-alt.jpg",
        "location_label": "Alger Centre",
        "city": "Alger",
        "country": "Algerie",
        "postal_code": "16000",
        "latitude": "36.7528",
        "longitude": "3.0420",
    }
    r_put = client.put("/api/plugins/config/restaurant", json=payload, headers=headers)
    assert r_put.status_code == 200, r_put.text
    updated = r_put.json()
    assert updated["name"] == payload["name"]
    assert updated["tax_nif"] == payload["tax_nif"]
    assert updated["logo_url"] == payload["logo_url"]

    r_get_final = client.get("/api/plugins/config/restaurant", headers=headers)
    assert r_get_final.status_code == 200, r_get_final.text
    final_state = r_get_final.json()
    assert final_state["name"] == payload["name"]
    assert final_state["address"] == payload["address"]
