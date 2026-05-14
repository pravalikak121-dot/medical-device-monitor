import random
from datetime import datetime


def calculate_status(battery_level: int, signal_strength: int) -> str:
    """Calculate simulated healthcare device status."""
    if battery_level <= 15 or signal_strength <= 25:
        return "Offline"
    if battery_level <= 30 or signal_strength <= 40:
        return "Warning"
    return "Online"


def generate_device(device_id: str) -> dict:
    """Generate simulated healthcare device telemetry."""
    battery_level = random.randint(10, 100)
    signal_strength = random.randint(20, 100)
    status = calculate_status(battery_level, signal_strength)

    return {
        "device_id": device_id,
        "patient_id": f"PAT-{random.randint(100, 999)}",
        "device_type": "Sleep Therapy Monitor",
        "status": status,
        "battery_level": battery_level,
        "signal_strength": signal_strength,
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def generate_devices(count: int = 8) -> list[dict]:
    """Generate multiple simulated healthcare devices."""
    return [generate_device(f"DEV-{1000 + index}") for index in range(1, count + 1)]


def generate_alerts_for_device(device: dict) -> list[dict]:
    """Generate alerts based on battery, signal, and device status."""
    alerts = []

    if device["battery_level"] <= 30:
        alerts.append(
            {
                "device_id": device["device_id"],
                "alert_type": "Low Battery",
                "severity": "Medium",
                "message": "Battery level is below 30%",
            }
        )

    if device["signal_strength"] <= 40:
        alerts.append(
            {
                "device_id": device["device_id"],
                "alert_type": "Weak Signal",
                "severity": "Medium",
                "message": "Signal strength is below 40%",
            }
        )

    if device["status"] == "Offline":
        alerts.append(
            {
                "device_id": device["device_id"],
                "alert_type": "Device Offline",
                "severity": "High",
                "message": "Device is currently offline",
            }
        )

    return alerts
