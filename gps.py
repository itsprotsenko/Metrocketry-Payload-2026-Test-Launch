import serial

class GPS:
    def __init__(self, port="/dev/ttyS0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=0.1)

    def parse_gngll(self, line):
        try:
            parts = line.split(',')
            if not parts[0].endswith("GLL"):
                return None

            # Latitude: DDMM.MMMMM
            lat_raw = parts[1]
            lat_dir = parts[2]
            # Longitude: DDDMM.MMMMM
            lon_raw = parts[3]
            lon_dir = parts[4]

            if not lat_raw or not lon_raw:
                return None

            # NMEA format is degrees + minutes.
            # Latitude uses 2 digits for degrees, Longitude uses 3.
            lat = float(lat_raw[:2]) + float(lat_raw[2:]) / 60
            lon = float(lon_raw[:3]) + float(lon_raw[3:]) / 60

            if lat_dir == "S": lat = -lat
            if lon_dir == "W": lon = -lon

            return {
                "lat": lat,
                "lon": lon,
                "time": parts[5],
                "status": parts[6]
            }
        except Exception as e:
            return None

    def read(self):
        """Reads the serial buffer until GNGLL is found or buffer is empty."""
        try:
            # Check if there is data waiting in the serial buffer
            while self.ser.in_waiting > 0:
                line = self.ser.readline().decode(errors="ignore").strip()

                # If we find the GLL line, parse and return it immediately
                if "$GNGLL" in line:
                    data = self.parse_gngll(line)
                    if data:
                        return data
        except Exception as e:
            print(f"GPS Error: {e}")

        # If no GLL line was found in this cycle, return the last known state
        return {}
