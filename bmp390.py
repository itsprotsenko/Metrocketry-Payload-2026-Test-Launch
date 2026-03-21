import board
import busio
import adafruit_bmp3xx

class BMP390:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_bmp3xx.BMP3XX_I2C(i2c)
        self.sensor.sea_level_pressure = 1013.25

    def read(self):
        return {
            "temperature": self.sensor.temperature,
            "pressure": self.sensor.pressure,
            "altitude": self.sensor.altitude
        }
