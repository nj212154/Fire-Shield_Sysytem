"""
serial_reader.py
Reads JSON lines from the Arduino over USB Serial and
POSTs each reading to the FastAPI backend.

Requirements:
    pip install pyserial httpx
"""

import serial
import serial.tools.list_ports
import httpx
import json
import time
import sys

# ─── Config ────────────────────────────────────────────────────────────────
SERIAL_PORT  = "COM3"          
                              # Leave None to auto-detect Arduino
BAUD_RATE    = 9600
API_URL      = "http://localhost:8000/api/sensors/data"
RECONNECT_S  = 3             # seconds between reconnect attempts


def find_arduino_port():
    """Auto-detect the first Arduino / USB serial device."""
    ports = serial.tools.list_ports.comports()
    for p in ports:
        desc = (p.description or "").lower()
        if any(k in desc for k in ("arduino", "ch340", "cp210", "ftdi", "usb serial")):
            print(f"[AUTO] Found device: {p.device} — {p.description}")
            return p.device
    # Fallback: return the first available port
    if ports:
        print(f"[AUTO] Using first available port: {ports[0].device}")
        return ports[0].device
    return None


def post_reading(client: httpx.Client, data: dict):
    try:
        r = client.post(API_URL, json=data, timeout=3)
        if r.status_code == 201:
            aq = "?" 
            # Quick air quality label for console
            sl = data.get("smoke_level", 0)
            if sl < 200:   aq = "Good"
            elif sl < 350: aq = "Moderate"
            elif sl < 500: aq = "Poor"
            else:          aq = "DANGEROUS"
            alarm = "⚠ ALARM" if data.get("alarm_active") else "✓"
            print(f"[OK]  smoke={sl:4d}  {aq:<10}  {alarm}")
        else:
            print(f"[ERR] HTTP {r.status_code}: {r.text[:80]}")
    except httpx.RequestError as e:
        print(f"[ERR] Cannot reach backend: {e}")


def run():
    port = SERIAL_PORT or find_arduino_port()
    if not port:
        print("[ERR] No serial port found. Plug in the Arduino and retry.")
        sys.exit(1)

    print(f"[INFO] Connecting to Arduino on {port} at {BAUD_RATE} baud…")
    print(f"[INFO] Posting data to {API_URL}")
    print("-" * 60)

    with httpx.Client() as client:
        while True:
            try:
                with serial.Serial(port, BAUD_RATE, timeout=2) as ser:
                    print(f"[INFO] Serial port open. Waiting for data…\n")
                    while True:
                        raw = ser.readline().decode("utf-8", errors="ignore").strip()
                        if not raw:
                            continue
                        try:
                            data = json.loads(raw)
                            # Skip the startup status message
                            if "status" in data:
                                print(f"[DEVICE] {data.get('msg', '')}")
                                continue
                            post_reading(client, data)
                        except json.JSONDecodeError:
                            pass  # Ignore non-JSON lines (startup noise etc.)

            except serial.SerialException as e:
                print(f"[WARN] Serial error: {e}. Reconnecting in {RECONNECT_S}s…")
                time.sleep(RECONNECT_S)


if __name__ == "__main__":
    run()