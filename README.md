# Test Launch Payload Telemtry Recording System

This project is a Python-based telemetry logger designed for a Raspberry Pi. It captures synchronized video, GPS coordinates, atmospheric data (pressure/altitude), motion data (acceleration/gyroscope), and monitors battery health via a UPS.

---

## Hardware Requirements

To use this software as written, you will need:
* **Raspberry Pi** (4B model was used for this)
* **Camera:** USB Webcam or CSI camera (via `v4l2` support)
* **GPS Module:** Connected via Serial (`/dev/ttyS0`)
* **BMP280 / BMP390:** Pressure & Temperature sensor (I2C)
* **MPU6050:** 6-Axis Accelerometer & Gyroscope (I2C)
* **UPS:** Waveshare UPS HAT (I2C address `0x42`)

---

## Setup & Installation

### 1. Enable Interfaces
Ensure I2C and Serial are enabled on your Raspberry Pi:
```bash
sudo raspi-config
```
* Navigate to **Interface Options** -> **I2C** -> **Enable**.
* Navigate to **Interface Options** -> **Serial Port** -> **No** (Login shell) -> **Yes** (Hardware enabled).
* Reboot your Pi.

### 2. Install System Dependencies
The camera module relies on `FFmpeg` and `v4l2-utils` for high-performance MJPG recording.
```bash
sudo apt update
sudo apt install ffmpeg v4l-utils python3-pip -y
```

### 3. Install Python Libraries
Install the necessary Adafruit and hardware-specific libraries:
```bash
pip3 install adafruit-circuitpython-bmp280 \
            adafruit-circuitpython-bmp3xx \
            mpu6050-raspberrypi \
            pyserial \
            smbus2 \
            adafruit-blinka
```

You may need to create a python virtual enviormnemnt to use pip in some cases. For this navigate to to location where you cloned this repository and create a python virtual enviormnemnt with:
```bash
python3 venv venv
```

And source the virtual environment with:
```bash
python3 source venv/bin/activate
```

---

## Project Structure

| File | Description |
| :--- | :--- |
| `main.py` | The entry point. Manages the loop, sensors, and safety shutdowns. |
| `camera.py` | Triggers FFmpeg to record 720p60 video in the background. |
| `logger.py` | Saves telemetry data into a structured `telemetry.json` file. |
| `gps.py` | Parses NMEA GNGLL strings for Lat/Lon coordinates. |
| `ups.py` | Monitors battery voltage, current, and percentage. |
| `bmp280.py` / `bmp390.py` | Handles atmospheric pressure and altitude. |
| `mpu_6050.py` | Captures motion and orientation data. |

---

## How to Run

1.  **Clone the repository** to your Raspberry Pi.
2.  **Navigate** to the project folder.
3.  **Run the script**:
*   **Note**: if you made a python virtual enviroment to use pip previously you will need to source the virtual enviroment before runnning.
    ```bash
    python3 main.py
    ```

### Safety Features
* **Graceful Shutdown:** Press `Ctrl+C` to stop. The script will send a 'q' signal to FFmpeg to ensure the video file is finalized and not corrupted.
* **Battery Protection:** If the UPS detects the battery falling below **50%**, the system will automatically stop recording and shut down the script to prevent data loss or SD card corruption.

---

## 📊 Output Data
After a session, you will find two main files in the directory:
1.  `output.mp4`: The recorded video (720p at 60fps).
2.  `telemetry.json`: A timestamped log of all sensor readings including GPS, altitude, and G-force.

---

## 🔧 Customization
* **Change Sensors:** If you are using a BMP390 instead of a 280, simply swap the import in `main.py` from `from bmp280 import BMP280` to `from bmp390 import BMP390`.
* **Adjust Thresholds:** You can modify the battery shutdown percentage in the `while running` loop inside `main.py`.
