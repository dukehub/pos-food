import asyncio
from app.core.events import event_bus, Event


def test_event_bus():
    received_events = []

    async def handle_test_event(event: Event):
        received_events.append(event)

    event_bus.subscribe("test.event", handle_test_event)

    payload = {"data": "test_data"}
    asyncio.run(event_bus.publish(Event(name="test.event", payload=payload)))

    assert len(received_events) == 1
    assert received_events[0].name == "test.event"
    assert received_events[0].payload == payload


def test_setup_endpoint(client):
    # Prepare setup data
    setup_data = {
        "tenant_name": "Test Restaurant",
        "tenant_slug": "test-restaurant",
        "admin_username": "admin",
        "admin_password": "securepassword",
        "admin_name": "Admin User"
    }

    # Clean up potentially conflicting data (if using a persistent DB for tests, though usually tests use a fresh DB or rollback)
    # logic depends on fixture implementation. Assuming standard pytest-asyncio behavior.
    
    response = client.post("/api/setup", json=setup_data)
    
    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Setup completed successfully"
    assert "tenant_id" in data

    # Verify duplicates are rejected
    response_duplicate = client.post("/api/setup", json=setup_data)
    assert response_duplicate.status_code == 400
    assert response_duplicate.json()["detail"] == "Application already set up"
