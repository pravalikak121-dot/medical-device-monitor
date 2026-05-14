from fastapi.testclient import TestClient

from app.main import app
from app.simulator import calculate_status, generate_alerts_for_device


client = TestClient(app)


def test_health_check_returns_healthy_status():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_get_devices_returns_list():
    response = client.get("/devices")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_get_single_device_returns_device():
    devices = client.get("/devices").json()
    device_id = devices[0]["device_id"]

    response = client.get(f"/devices/{device_id}")

    assert response.status_code == 200
    assert response.json()["device_id"] == device_id


def test_create_device_successfully():
    payload = {
        "device_id": "DEV-TEST-001",
        "patient_id": "PAT-TEST",
        "device_type": "Sleep Therapy Monitor",
        "battery_level": 88,
        "signal_strength": 90,
    }

    response = client.post("/devices", json=payload)

    assert response.status_code in [201, 409]


def test_get_alerts_returns_list():
    response = client.get("/alerts")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_calculate_status_online():
    assert calculate_status(90, 90) == "Online"


def test_calculate_status_warning():
    assert calculate_status(25, 80) == "Warning"


def test_calculate_status_offline():
    assert calculate_status(10, 80) == "Offline"


def test_low_battery_alert_generated():
    device = {
        "device_id": "DEV-LOW-BATTERY",
        "battery_level": 20,
        "signal_strength": 90,
        "status": "Warning",
    }

    alerts = generate_alerts_for_device(device)

    assert any(alert["alert_type"] == "Low Battery" for alert in alerts)
