import smbus2

class UPS:
    def __init__(self, bus=1, addr=0x42): # Waveshare UPS default is often 0x42 or 0x41
        self.bus = smbus2.SMBus(bus)
        self.addr = addr

        # Initialize the INA219 with a basic configuration if needed
        try:
            # Config: 32V range, 320mV Gain, 12-bit ADC
            self.bus.write_word_data(self.addr, 0x00, 0x399F)
        except:
            print(f"Warning: Could not connect to UPS at {hex(addr)}")

    def read_word(self, reg):
        try:
            val = self.bus.read_word_data(self.addr, reg)
            # INA219 is Big-Endian, SMBus read_word is Little-Endian. Swap them.
            return ((val & 0xFF) << 8) | (val >> 8)
        except:
            return None

    def read(self):
        try:
            # Bus Voltage Register (0x02)
            raw_bus_voltage = self.read_word(0x02)
            if raw_bus_voltage is None: return {}

            voltage = (raw_bus_voltage >> 3) * 0.004

            # Current Register (0x04)
            raw_current = self.read_word(0x04)
            if raw_current is not None:
                if raw_current > 32767: # Handle negative numbers (discharge)
                    raw_current -= 65536
                current = raw_current * 0.1 / 1000 # 0.1mA per LSB usually
            else:
                current = 0.0

            # Calculate Power and Percentage
            power = voltage * abs(current)

            percent = (voltage - 3.0) / 1.2 * 100
            percent = max(0, min(100, percent))

            return {
                "voltage": round(voltage, 2),
                "current": round(current, 3),
                "power": round(power, 3),
                "percentage": round(percent, 1)
            }
        except Exception as e:
            print(f"UPS Read Error: {e}")
            return {}
