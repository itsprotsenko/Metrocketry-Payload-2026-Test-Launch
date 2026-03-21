import board
import busio
import adafruit_bmp280

class BMP280:
    def __init__(self, address=0x76):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=address)

        # Optional calibration
        self.sensor.sea_level_pressure = 1013.25

    def read(self):
        return {
            "temperature": self.sensor.temperature,
            "pressure": self.sensor.pressure,
            "altitude": self.sensor.altitude
        }
