from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from datetime import datetime, timedelta

from models.sensor_reading import SensorReading
from schemas.sensor import SensorDataIn


async def save_reading(db: AsyncSession, data: SensorDataIn) -> SensorReading:
    reading = SensorReading(
        smoke_level=data.smoke_level,
        air_quality=data.air_quality,
        alarm_active=data.alarm_active,
        sprinkler_active=data.sprinkler_active,
        battery_percent=data.battery_percent,
        battery_voltage=data.battery_voltage,
        signal_strength=data.signal_strength,
        uptime=data.uptime,
        alert_count=data.alert_count,
        total_sprinkler_time=data.total_sprinkler_time,
        device_id=data.device_id,
        firmware_version=data.firmware_version,
        location=data.location,
    )
    db.add(reading)
    await db.commit()
    await db.refresh(reading)
    return reading


async def get_latest_reading(db: AsyncSession) -> SensorReading | None:
    result = await db.execute(
        select(SensorReading).order_by(desc(SensorReading.timestamp)).limit(1)
    )
    return result.scalar_one_or_none()


async def get_readings_history(db: AsyncSession, minutes: int = 60, limit: int = 120):
    since = datetime.utcnow() - timedelta(minutes=minutes)
    result = await db.execute(
        select(SensorReading)
        .where(SensorReading.timestamp >= since)
        .order_by(SensorReading.timestamp)
        .limit(limit)
    )
    return result.scalars().all()


async def count_readings_last_hour(db: AsyncSession) -> int:
    since = datetime.utcnow() - timedelta(hours=1)
    result = await db.execute(
        select(func.count(SensorReading.id))
        .where(SensorReading.timestamp >= since)
    )
    return result.scalar_one()