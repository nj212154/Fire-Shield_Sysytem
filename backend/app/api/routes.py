import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from schemas.sensor import SensorDataIn, SensorDataOut, DashboardStats, AlertOut
import random

router = APIRouter()

# In-memory storage (replace with database later)
readings: list = []
alerts: list = []
alert_id_counter: int = 0
reading_id_counter: int = 0

@router.post("/sensors/data", response_model=SensorDataOut, status_code=201)
def receive_sensor_data(data: SensorDataIn):
    global reading_id_counter
    reading_id_counter += 1
    
    reading = {
        "id": reading_id_counter,
        "device_id": data.device_id,
        "smoke_level": data.smoke_level,
        "air_quality": data.air_quality,
        "alarm_active": data.alarm_active,
        "sprinkler_active": data.sprinkler_active,
        "battery_percent": data.battery_percent,
        "battery_voltage": data.battery_voltage,
        "signal_strength": data.signal_strength,
        "uptime": data.uptime,
        "alert_count": data.alert_count,
        "total_sprinkler_time": data.total_sprinkler_time,
        "firmware_version": data.firmware_version,
        "location": data.location,
        "timestamp": data.timestamp or datetime.utcnow()
    }
    
    readings.append(reading)
    
    # If alarm is active, create an alert
    if data.alarm_active:
        global alert_id_counter
        alert_id_counter += 1
        alert = {
            "id": alert_id_counter,
            "device_id": data.device_id,
            "alert_type": "smoke_detected",
            "severity": "high" if data.smoke_level > 700 else "medium",
            "message": f"Smoke level {data.smoke_level} exceeds threshold",
            "smoke_level": data.smoke_level,
            "resolved": False,
            "timestamp": datetime.utcnow()
        }
        alerts.append(alert)
    
    return reading


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard():
    if not readings:
        # Return sample data if no readings yet
        return DashboardStats(
            smoke_level=0,
            air_quality="Good",
            alarm_active=False,
            sprinkler_active=False,
            battery_percent=100,
            battery_voltage=9.0,
            signal_strength=-50,
            uptime=0,
            alert_count=0,
            total_sprinkler_time=0,
            device_id="FS-001",
            firmware_version="1.0.0",
            location="Waiting for data...",
            last_updated=datetime.utcnow(),
            readings_last_hour=0,
            smoke_history=[]
        )
    
    latest = readings[-1]
    
    # Get last hour readings
    hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent = [r for r in readings if r["timestamp"] >= hour_ago]
    
    smoke_history = [
        {"timestamp": r["timestamp"].isoformat(), "smoke_level": r["smoke_level"]}
        for r in recent[-60:]  # Last 60 readings
    ]
    
    return DashboardStats(
        smoke_level=latest["smoke_level"],
        air_quality=latest["air_quality"],
        alarm_active=latest["alarm_active"],
        sprinkler_active=latest["sprinkler_active"],
        battery_percent=latest["battery_percent"],
        battery_voltage=latest["battery_voltage"],
        signal_strength=latest["signal_strength"],
        uptime=latest["uptime"],
        alert_count=latest["alert_count"],
        total_sprinkler_time=latest["total_sprinkler_time"],
        device_id=latest["device_id"],
        firmware_version=latest["firmware_version"],
        location=latest["location"],
        last_updated=latest["timestamp"],
        readings_last_hour=len(recent),
        smoke_history=smoke_history
    )


@router.get("/sensors/history", response_model=list[SensorDataOut])
def get_history(minutes: int = 60):
    since = datetime.utcnow() - timedelta(minutes=minutes)
    return [r for r in readings if r["timestamp"] >= since]


@router.get("/alerts", response_model=list[AlertOut])
def get_alerts():
    return alerts[-20:]  # Last 20 alerts


@router.post("/alerts/{alert_id}/resolve")
def resolve_alert(alert_id: int):
    for alert in alerts:
        if alert["id"] == alert_id:
            alert["resolved"] = True
            return {"message": "Alert resolved", "alert_id": alert_id}
    raise HTTPException(status_code=404, detail="Alert not found")