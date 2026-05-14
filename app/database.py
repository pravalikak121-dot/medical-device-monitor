from app.simulator import generate_devices, generate_alerts_for_device


# In-memory simulated database for portfolio/demo use.
devices = generate_devices()


def get_all_devices() -> list[dict]:
    return devices


def get_device_by_id(device_id: str) -> dict | None:
    for device in devices:
        if device["device_id"] == device_id:
            return device
    return None


def add_device(device: dict) -> dict:
    devices.append(device)
    return device


def update_device_status(device_id: str, status: str) -> dict | None:
    device = get_device_by_id(device_id)

    if device is None:
        return None

    device["status"] = status
    return device


def refresh_devices() -> list[dict]:
    global devices
    devices = generate_devices()
    return devices


def get_all_alerts() -> list[dict]:
    alerts = []

    for device in devices:
        alerts.extend(generate_alerts_for_device(device))

    return alerts
