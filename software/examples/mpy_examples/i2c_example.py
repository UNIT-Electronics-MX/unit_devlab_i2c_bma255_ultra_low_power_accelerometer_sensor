"""
BMA250 I2C Example for MicroPython
Based on Arduino implementation for UNIT Electronics BMA250 module

This example demonstrates how to use the BMA250 accelerometer with I2C communication.

Hardware connections:
- VCC → 3.3V
- GND → GND
- SDA → GPIO 6 (or change as needed)
- SCL → GPIO 7 (or change as needed)  
- SDO → GND (for address 0x18) or VCC (for address 0x19)

Compatible with:
- ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6
- Raspberry Pi Pico/Pico W
- PyBoard
- Other MicroPython boards with I2C support

Author: GitHub Copilot
Date: 2025-09-08
"""

from machine import I2C, Pin
import time
from bma250 import BMA250

# I2C pins configuration (adjust for your board)
# ESP32/ESP32-C6 example:
SDA_PIN = 6
SCL_PIN = 7

# Raspberry Pi Pico example:
# SDA_PIN = 4
# SCL_PIN = 5

def main():
    print("=== BMA250 I2C MicroPython Example ===")
    
    # Initialize I2C
    try:
        i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
        print(f"I2C initialized with SDA=GPIO{SDA_PIN}, SCL=GPIO{SCL_PIN}")
    except Exception as e:
        print(f"ERROR: Failed to initialize I2C: {e}")
        return
    
    # Create BMA250 sensor object
    accel_sensor = BMA250()
    
    # Initialize sensor with I2C
    print("Initializing BMA250 via I2C...")
    if not accel_sensor.begin_i2c(i2c, BMA250.RANGE_2G, BMA250.UPDATE_TIME_64MS):
        print("FAILED to initialize BMA250!")
        print("\nTroubleshooting:")
        print("1. Check wiring connections")
        print("2. Verify power supply (3.3V)")
        print("3. Check I2C address (SDO pin)")
        
        # Scan I2C bus for debugging
        accel_sensor.scan_i2c_devices()
        return
    
    print("SUCCESS! BMA250 initialized")
    print("=====================================")
    print("Reading sensor data...")
    print("(Press Ctrl+C to stop)\n")
    
    try:
        while True:
            # Read sensor data
            accel_sensor.read()
            
            # Check if sensor is responding
            if accel_sensor.x == -1 and accel_sensor.y == -1 and accel_sensor.z == -1:
                print("ERROR! No BMA250 detected via I2C!")
                print("Check connections:")
                print(f"- SDA → GPIO{SDA_PIN}")
                print(f"- SCL → GPIO{SCL_PIN}")
                print("- SDO → GND (addr 0x18) or VCC (addr 0x19)")
                break
            
            # Print sensor readings
            accel_sensor.print_status()
            
            # Optional: Print acceleration in mg
            x_mg, y_mg, z_mg = accel_sensor.get_acceleration_mg(BMA250.RANGE_2G)
            print(f"Acceleration: X={x_mg:.1f}mg, Y={y_mg:.1f}mg, Z={z_mg:.1f}mg")
            print()
            
            # Wait before next reading
            time.sleep(0.25)
            
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"ERROR: {e}")

def test_i2c_scan():
    """Standalone function to scan I2C bus for debugging"""
    print("=== I2C Bus Scanner ===")
    
    try:
        i2c = I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)
        devices = i2c.scan()
        
        if devices:
            print("I2C devices found:")
            for device in devices:
                print(f"  0x{device:02X}")
        else:
            print("No I2C devices found")
            print("Check connections and power supply")
    except Exception as e:
        print(f"ERROR: Failed to scan I2C bus: {e}")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to run I2C scanner instead
    # test_i2c_scan()
