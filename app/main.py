from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.database import (
    add_device,
    get_all_alerts,
    get_all_devices,
    get_device_by_id,
    refresh_devices,
    update_device_status,
)
from app.simulator import calculate_status


app = FastAPI(
    title="Healthcare Device Monitoring API",
    description="A simulated healthcare device monitoring backend for portfolio use.",
    version="1.0.0",
)


class DeviceCreate(BaseModel):
    device_id: str = Field(..., example="DEV-2001")
    patient_id: str = Field(..., example="PAT-501")
    device_type: str = Field(default="Sleep Therapy Monitor")
    battery_level: int = Field(..., ge=0, le=100, example=87)
    signal_strength: int = Field(..., ge=0, le=100, example=92)


class StatusUpdate(BaseModel):
    status: str = Field(..., example="Online")


@app.get("/")
def root():
    return {
        "message": "Healthcare Device Monitoring API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/devices")
def get_devices():
    return get_all_devices()


@app.get("/devices/{device_id}")
def get_device(device_id: str):
    device = get_device_by_id(device_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@app.post("/devices", status_code=201)
def create_device(device: DeviceCreate):
    existing_device = get_device_by_id(device.device_id)

    if existing_device:
        raise HTTPException(status_code=409, detail="Device already exists")

    device_data = device.model_dump()
    device_data["status"] = calculate_status(
        device.battery_level,
        device.signal_strength,
    )
    device_data["last_sync"] = "Created by API request"

    return add_device(device_data)


@app.put("/devices/{device_id}/status")
def change_device_status(device_id: str, status_update: StatusUpdate):
    updated_device = update_device_status(device_id, status_update.status)

    if updated_device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return updated_device


@app.get("/alerts")
def get_alerts():
    return get_all_alerts()


@app.post("/devices/simulate")
def simulate_devices():
    refreshed_devices = refresh_devices()
    return {
        "message": "Device telemetry refreshed successfully",
        "devices": refreshed_devices,
    }
