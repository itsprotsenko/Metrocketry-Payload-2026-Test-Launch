import time
import signal
import sys

from camera import Camera
from bmp280 import BMP280
from mpu_6050 import MPU6050
from gps import GPS
from ups import UPS
from logger import Logger

running = True

def signal_handler(sig, frame):
    global running
    print("\nManual stop detected (Ctrl+C)...")
    running = False

def main():
    global running

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    cam = Camera()
    bmp = BMP280()
    mpu = MPU6050()
    gps = GPS()
    ups = UPS()
    logger = Logger()

    print("System started. Monitoring battery...")

    try:
        while running:
            # Read all sensors
            ups_data = ups.read()

            telemetry = {
                "bmp390": bmp.read(),
                "mpu6050": mpu.read(),
                "gps": gps.read(),
                "ups": ups_data
            }

            # Check Battery Shutdown Condition
            battery_pct = ups_data.get("percentage", 100)

            if 0 < battery_pct < 50:
                print(f"!!! Battery Low ({battery_pct}%). Shutting down system safely...")
                running = False
                continue # Skip logging and sleep to exit immediately

            # Log data
            logger.log(telemetry)

            time.sleep(1)

    except Exception as e:
        print(f"Unexpected Error: {e}")

    finally:
        print("Cleaning up hardware and saving files...")
        cam.release()
        logger.close()
        print("Shutdown complete.")
        sys.exit(0)

if __name__ == "__main__":
    main()
