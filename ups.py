import smbus
import time

class UPS:
    def __init__(self, bus=1, addr=0x42):
        self.bus = smbus.SMBus(bus)
        self.addr = addr

        self._cal_value = 26868
        self._current_lsb = 0.1524
        self._power_lsb = 0.003048

        self.initialize_ina219()

    def write_reg(self, address, data):
        temp = [0, 0]
        temp[1] = data & 0xFF
        temp[0] = (data & 0xFF00) >> 8
        self.bus.write_i2c_block_data(self.addr, address, temp)

    def read_reg(self, address):
        data = self.bus.read_i2c_block_data(self.addr, address, 2)
        return ((data[0] * 256) + data[1])

    def initialize_ina219(self):
        try:
            # Set Calibration register
            self.write_reg(0x05, self._cal_value)

            # Config settings: Range 16V, Gain /2 (80mV), 12-bit ADC (32 samples)
            # Binary: 0 [Bus 16V] [Gain /2] [Bus Res] [Shunt Res] [Mode Continuous]
            config = (0x00 << 13) | (0x01 << 11) | (0x0F << 7) | (0x0F << 3) | 0x07
            self.write_reg(0x00, config)
        except Exception as e:
            print(f"UPS Initialization Error: {e}")

    def read(self):
        try:
            self.write_reg(0x05, self._cal_value)

            # Bus Voltage
            raw_v = self.read_reg(0x02)
            voltage = (raw_v >> 3) * 0.004

            # Current
            raw_current = self.read_reg(0x04)
            if raw_current > 32767:
                raw_current -= 65535
            current_ma = raw_current * self._current_lsb
            current_a = current_ma / 1000

            # Power
            raw_power = self.read_reg(0x03)
            if raw_power > 32767:
                raw_power -= 65535
            power_w = raw_power * self._power_lsb

            # Percentage calculation based on Waveshare 2S LiPo (6.0V - 8.4V)
            percent = (voltage - 6.0) / 2.4 * 100
            percent = max(0, min(100, percent))

            return {
                "voltage": round(voltage, 3),
                "current_a": round(current_a, 4),
                "power_w": round(power_w, 3),
                "percentage": round(percent, 1)
            }
        except Exception as e:
            print(f"UPS Read Error: {e}")
            return {}
