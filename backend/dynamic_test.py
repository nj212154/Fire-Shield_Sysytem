import requests, time, random

url = "http://localhost:8000/api/sensors/data"
state = "safe"
count = 0

while True:
    if state == "safe":
        smoke = random.randint(50, 250)
        alarm = False
        sprinkler = False
        air = "Good"
        # randomly trigger alarm after 10-20 readings
        count += 1
        if count > random.randint(10, 20):
            state = "ramp_up"
            count = 0
    elif state == "ramp_up":
        smoke = random.randint(350, 500)
        alarm = smoke > 400
        sprinkler = alarm
        air = "Moderate" if smoke < 400 else "Poor"
        count += 1
        if count > 3:
            state = "critical"
            count = 0
    elif state == "critical":
        smoke = random.randint(600, 900)
        alarm = True
        sprinkler = True
        air = "Dangerous"
        count += 1
        if count > 4:
            state = "recovery"
            count = 0
    else:  # recovery
        smoke = random.randint(100, 300)
        alarm = False
        sprinkler = False
        air = "Good" if smoke < 200 else "Moderate"
        count += 1
        if count > 5:
            state = "safe"
            count = 0

    payload = {
        "device_id": "FS-001",
        "smoke_level": smoke,
        "air_quality": air,
        "alarm_active": alarm,
        "sprinkler_active": sprinkler,
        "battery_percent": random.randint(75, 85),
        "battery_voltage": round(random.uniform(7.4, 8.4), 1),
        "signal_strength": random.randint(-75, -55),
        "uptime": int(time.time()) % 10000,
        "alert_count": 2,
        "total_sprinkler_time": 45,
        "firmware_version": "1.0.0",
        "location": "Building A"
    }
    requests.post(url, json=payload)
    time.sleep(2)  # new reading every 2 seconds