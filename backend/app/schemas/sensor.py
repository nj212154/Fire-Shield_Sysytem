from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# Data coming FROM Arduino
class SensorDataIn(BaseModel):
    device_id: str
    smoke_level: int
    air_quality: str
    alarm_active: bool = False
    sprinkler_active: bool = False
    battery_percent: int = 0
    battery_voltage: float = 0.0
    signal_strength: int = 0
    uptime: int = 0
    alert_count: int = 0
    total_sprinkler_time: int = 0
    firmware_version: str = "1.0.0"
    location: str = ""
    timestamp: Optional[datetime] = None

# Data returned TO dashboard
class SensorDataOut(BaseModel):
    id: int
    device_id: str
    smoke_level: int
    air_quality: str
    alarm_active: bool
    sprinkler_active: bool
    battery_percent: int
    battery_voltage: float
    signal_strength: int
    uptime: int
    alert_count: int
    total_sprinkler_time: int
    firmware_version: str
    location: str
    timestamp: datetime

    class Config:
        from_attributes = True

# Dashboard stats
class DashboardStats(BaseModel):
    smoke_level: int
    air_quality: str
    alarm_active: bool
    sprinkler_active: bool
    battery_percent: int
    battery_voltage: float
    signal_strength: int
    uptime: int
    alert_count: int
    total_sprinkler_time: int
    device_id: str
    firmware_version: str
    location: str
    last_updated: datetime
    readings_last_hour: int = 0
    smoke_history: List[dict] = []

# Alert data
class AlertOut(BaseModel):
    id: int
    device_id: str
    alert_type: str
    severity: str
    message: str
    smoke_level: int
    resolved: bool
    timestamp: datetime

    class Config:
        from_attributes = True