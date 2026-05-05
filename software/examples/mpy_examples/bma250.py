"""
BMA250 Accelerometer Library for MicroPython
Based on Arduino implementation for UNIT Electronics BMA250 module

Author: GitHub Copilot
Date: 2025-09-08
License: MIT

Hardware connections:
I2C:
- VCC → 3.3V
- GND → GND  
- SDA → GPIO pin (configurable)
- SCL → GPIO pin (configurable)
- SDO → GND (for address 0x18) or VCC (for address 0x19)

SPI:
- VCC → 3.3V
- GND → GND
- SCK → SPI SCK pin
- MOSI → SPI MOSI pin
- MISO → SPI MISO pin
- CS → GPIO pin (configurable)
"""

from machine import I2C, SPI, Pin
import time
import struct

class BMA250:
    # I2C Configuration
    I2C_ADDR_DEFAULT = 0x18
    I2C_ADDR_ALT = 0x19
    
    # SPI Configuration
    SPI_READ = 0x80
    SPI_WRITE = 0x00
    
    # Register definitions
    REG_CHIPID = 0x00
    REG_RANGE = 0x0F
    REG_BW = 0x10
    REG_X_LSB = 0x02
    REG_X_MSB = 0x03
    REG_Y_LSB = 0x04
    REG_Y_MSB = 0x05
    REG_Z_LSB = 0x06
    REG_Z_MSB = 0x07
    REG_TEMP = 0x08
    
    # Update time settings
    UPDATE_TIME_64MS = 0x08
    UPDATE_TIME_32MS = 0x09
    UPDATE_TIME_16MS = 0x0A
    UPDATE_TIME_8MS = 0x0B
    UPDATE_TIME_4MS = 0x0C
    UPDATE_TIME_2MS = 0x0D
    UPDATE_TIME_1MS = 0x0E
    UPDATE_TIME_05MS = 0x0F
    
    # Range settings
    RANGE_2G = 0x03
    RANGE_4G = 0x05
    RANGE_8G = 0x08
    RANGE_16G = 0x0C
    
    # Communication modes
    MODE_I2C = 0
    MODE_SPI = 1
    
    def __init__(self):
        """Initialize BMA250 sensor object"""
        self._mode = self.MODE_I2C
        self._i2c = None
        self._spi = None
        self._cs_pin = None
        self._i2c_addr = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.raw_temp = 0
        self.temp_c = 0
    
    def begin_i2c(self, i2c, range_setting=None, bandwidth=None, i2c_addr=None):
        """
        Initialize BMA250 with I2C communication
        
        Args:
            i2c: I2C object (machine.I2C)
            range_setting: Acceleration range (default: RANGE_2G)
            bandwidth: Bandwidth setting (default: UPDATE_TIME_64MS)
            i2c_addr: I2C address (default: auto-detect)
            
        Returns:
            True if successful, False otherwise
        """
        if range_setting is None:
            range_setting = self.RANGE_2G
        if bandwidth is None:
            bandwidth = self.UPDATE_TIME_64MS
            
        self._mode = self.MODE_I2C
        self._i2c = i2c
        
        # Auto-detect I2C address if not provided
        if i2c_addr is None:
            for addr in [self.I2C_ADDR_DEFAULT, self.I2C_ADDR_ALT]:
                try:
                    self._i2c.writeto(addr, bytes([self.REG_CHIPID]))
                    self._i2c_addr = addr
                    break
                except OSError:
                    continue
            else:
                print("ERROR: BMA250 not found on I2C bus")
                return False
        else:
            self._i2c_addr = i2c_addr
            
        # Verify communication by reading chip ID
        try:
            chip_id = self._read_register(self.REG_CHIPID)
            if chip_id == 0x00 or chip_id == 0xFF:
                print(f"ERROR: Invalid chip ID: 0x{chip_id:02X}")
                return False
            print(f"BMA250 detected with chip ID: 0x{chip_id:02X}")
        except Exception as e:
            print(f"ERROR: Failed to read chip ID: {e}")
            return False
            
        # Configure range and bandwidth
        self._write_register(self.REG_RANGE, range_setting)
        self._write_register(self.REG_BW, bandwidth)
        
        print(f"BMA250 initialized via I2C at address 0x{self._i2c_addr:02X}")
        return True
    
    def begin_spi(self, spi, cs_pin, range_setting=None, bandwidth=None):
        """
        Initialize BMA250 with SPI communication
        
        Args:
            spi: SPI object (machine.SPI)
            cs_pin: Chip Select pin (machine.Pin)
            range_setting: Acceleration range (default: RANGE_2G)
            bandwidth: Bandwidth setting (default: UPDATE_TIME_64MS)
            
        Returns:
            True if successful, False otherwise
        """
        if range_setting is None:
            range_setting = self.RANGE_2G
        if bandwidth is None:
            bandwidth = self.UPDATE_TIME_64MS
            
        self._mode = self.MODE_SPI
        self._spi = spi
        self._cs_pin = cs_pin
        
        # Configure CS pin
        self._cs_pin.init(Pin.OUT)
        self._cs_pin.value(1)
        
        # Verify communication by reading chip ID
        try:
            chip_id = self._read_register(self.REG_CHIPID)
            if chip_id == 0x00 or chip_id == 0xFF:
                print(f"ERROR: Invalid chip ID: 0x{chip_id:02X}")
                return False
            print(f"BMA250 detected with chip ID: 0x{chip_id:02X}")
        except Exception as e:
            print(f"ERROR: Failed to read chip ID: {e}")
            return False
            
        # Configure range and bandwidth
        self._write_register(self.REG_RANGE, range_setting)
        self._write_register(self.REG_BW, bandwidth)
        
        print("BMA250 initialized via SPI")
        return True
    
    def read(self):
        """
        Read acceleration and temperature data from sensor
        Updates x, y, z, raw_temp, and temp_c attributes
        """
        try:
            # Read 7 bytes starting from X_LSB register
            data = self._read_multiple_registers(self.REG_X_LSB, 7)
            
            # Combine LSB and MSB for each axis
            self.x = struct.unpack('<h', data[0:2])[0]
            self.y = struct.unpack('<h', data[2:4])[0]
            self.z = struct.unpack('<h', data[4:6])[0]
            
            # Only use the 10 significant bits (shift right by 6)
            self.x >>= 6
            self.y >>= 6
            self.z >>= 6
            
            # Read temperature
            self.raw_temp = struct.unpack('b', data[6:7])[0]  # signed byte
            self.temp_c = self.raw_temp // 2 + 23
            
        except Exception as e:
            print(f"ERROR: Failed to read sensor data: {e}")
            self.x = self.y = self.z = -1
            self.raw_temp = 0
            self.temp_c = 0
    
    def get_acceleration_mg(self, range_setting=None):
        """
        Get acceleration values in mg (milligravity)
        
        Args:
            range_setting: Current range setting (default: RANGE_2G)
            
        Returns:
            tuple: (x_mg, y_mg, z_mg)
        """
        if range_setting is None:
            range_setting = self.RANGE_2G
            
        # Determine scale factor based on range
        if range_setting == self.RANGE_2G:
            scale = 2000 / 512  # 2g range, 10-bit resolution
        elif range_setting == self.RANGE_4G:
            scale = 4000 / 512  # 4g range, 10-bit resolution
        elif range_setting == self.RANGE_8G:
            scale = 8000 / 512  # 8g range, 10-bit resolution
        elif range_setting == self.RANGE_16G:
            scale = 16000 / 512  # 16g range, 10-bit resolution
        else:
            scale = 2000 / 512  # default to 2g
            
        x_mg = self.x * scale
        y_mg = self.y * scale
        z_mg = self.z * scale
        
        return (x_mg, y_mg, z_mg)
    
    def scan_i2c_devices(self):
        """
        Scan I2C bus for devices (useful for debugging)
        
        Returns:
            list: List of found I2C addresses
        """
        if self._mode != self.MODE_I2C or self._i2c is None:
            print("ERROR: I2C not initialized")
            return []
            
        print("Scanning I2C bus...")
        devices = self._i2c.scan()
        
        if devices:
            print("I2C devices found:")
            for device in devices:
                print(f"  0x{device:02X}")
        else:
            print("No I2C devices found")
            
        return devices
    
    def _write_register(self, reg, value):
        """Write a single register"""
        if self._mode == self.MODE_I2C:
            self._i2c.writeto(self._i2c_addr, bytes([reg, value]))
        else:  # SPI mode
            self._cs_pin.value(0)
            self._spi.write(bytes([reg | self.SPI_WRITE, value]))
            self._cs_pin.value(1)
    
    def _read_register(self, reg):
        """Read a single register"""
        if self._mode == self.MODE_I2C:
            self._i2c.writeto(self._i2c_addr, bytes([reg]))
            data = self._i2c.readfrom(self._i2c_addr, 1)
            return data[0]
        else:  # SPI mode
            self._cs_pin.value(0)
            result = bytearray(2)
            self._spi.write_readinto(bytes([reg | self.SPI_READ, 0x00]), result)
            self._cs_pin.value(1)
            return result[1]
    
    def _read_multiple_registers(self, reg, length):
        """Read multiple consecutive registers"""
        if self._mode == self.MODE_I2C:
            self._i2c.writeto(self._i2c_addr, bytes([reg]))
            return self._i2c.readfrom(self._i2c_addr, length)
        else:  # SPI mode
            data = bytearray(length)
            for i in range(length):
                self._cs_pin.value(0)
                result = bytearray(2)
                self._spi.write_readinto(bytes([(reg + i) | self.SPI_READ, 0x00]), result)
                self._cs_pin.value(1)
                data[i] = result[1]
                time.sleep_us(1)  # Small delay between SPI transactions
            return data

    def print_status(self):
        """Print current sensor readings in a formatted way"""
        print(f"X = {self.x:4d}  Y = {self.y:4d}  Z = {self.z:4d}  Temperature(C) = {self.temp_c}")
