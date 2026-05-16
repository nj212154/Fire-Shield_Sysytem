from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.sql import func
from database.connection import Base


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    smoke_level = Column(Integer, nullable=False)
    air_quality = Column(String, nullable=False)
    alarm_active = Column(Boolean, default=False)
    sprinkler_active = Column(Boolean, default=False)
    battery_percent = Column(Integer, default=0)
    battery_voltage = Column(Float, default=0.0)
    signal_strength = Column(Integer, default=0)
    uptime = Column(Integer, default=0)
    alert_count = Column(Integer, default=0)
    total_sprinkler_time = Column(Integer, default=0)
    device_id = Column(String, index=True)
    firmware_version = Column(String, default="1.0.0")
    location = Column(String, default="")
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)