"""
BMA250 SPI Example for MicroPython
Based on Arduino implementation for UNIT Electronics BMA250 module

This example demonstrates how to use the BMA250 accelerometer with SPI communication.

Hardware connections:
- VCC → 3.3V
- GND → GND
- SCK → SPI SCK pin (GPIO 18 on ESP32)
- MOSI → SPI MOSI pin (GPIO 23 on ESP32) 
- MISO → SPI MISO pin (GPIO 19 on ESP32)
- CS → GPIO pin (configurable, GPIO 5 in this example)

Compatible with:
- ESP32, ESP32-S2, ESP32-S3, ESP32-C3, ESP32-C6
- Raspberry Pi Pico/Pico W
- PyBoard
- Other MicroPython boards with SPI support

Author: GitHub Copilot
Date: 2025-09-08
"""

from machine import SPI, Pin
import time
from bma250 import BMA250

# SPI pins configuration (adjust for your board)
# ESP32 example:
# SCK_PIN = 18
# MOSI_PIN = 23
# MISO_PIN = 19
# CS_PIN = 5

# ESP32-C6 example:
SCK_PIN = 6
MOSI_PIN = 7
MISO_PIN = 2
CS_PIN = 18

# Raspberry Pi Pico example:
# SCK_PIN = 18
# MOSI_PIN = 19
# MISO_PIN = 16
# CS_PIN = 17

def main():
    print("=== BMA250 SPI MicroPython Example ===")
    
    # Initialize SPI
    try:
        spi = SPI(1, baudrate=1000000, polarity=0, phase=0, 
                 sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
        cs_pin = Pin(CS_PIN, Pin.OUT)
        print(f"SPI initialized with SCK=GPIO{SCK_PIN}, MOSI=GPIO{MOSI_PIN}, MISO=GPIO{MISO_PIN}, CS=GPIO{CS_PIN}")
    except Exception as e:
        print(f"ERROR: Failed to initialize SPI: {e}")
        return
    
    # Create BMA250 sensor object
    accel_sensor = BMA250()
    
    # Initialize sensor with SPI
    print("Initializing BMA250 via SPI...")
    if not accel_sensor.begin_spi(spi, cs_pin, BMA250.RANGE_2G, BMA250.UPDATE_TIME_64MS):
        print("FAILED to initialize BMA250!")
        print("\nTroubleshooting:")
        print("1. Check wiring connections")
        print("2. Verify power supply (3.3V)")
        print("3. Check SPI connections:")
        print(f"   - SCK → GPIO{SCK_PIN}")
        print(f"   - MOSI → GPIO{MOSI_PIN}")
        print(f"   - MISO → GPIO{MISO_PIN}")
        print(f"   - CS → GPIO{CS_PIN}")
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
                print("ERROR! No BMA250 detected via SPI!")
                print("Check connections:")
                print(f"- SCK → GPIO{SCK_PIN}")
                print(f"- MOSI → GPIO{MOSI_PIN}")
                print(f"- MISO → GPIO{MISO_PIN}")
                print(f"- CS → GPIO{CS_PIN}")
                break
            
            # Print sensor readings
            accel_sensor.print_status()
            
            # Optional: Print acceleration in mg
            x_mg, y_mg, z_mg = accel_sensor.get_acceleration_mg(BMA250.RANGE_2G)
            print(f"Acceleration: X={x_mg:.1f}mg, Y={y_mg:.1f}mg, Z={z_mg:.1f}mg")
            
            # Optional: Print tilt detection
            print_tilt_detection(x_mg, y_mg, z_mg)
            print()
            
            # Wait before next reading
            time.sleep(0.25)
            
    except KeyboardInterrupt:
        print("\nStopped by user")
    except Exception as e:
        print(f"ERROR: {e}")

def print_tilt_detection(x_mg, y_mg, z_mg):
    """Simple tilt detection based on acceleration values"""
    threshold = 500  # mg threshold for tilt detection
    
    tilt_status = []
    
    if x_mg > threshold:
        tilt_status.append("RIGHT")
    elif x_mg < -threshold:
        tilt_status.append("LEFT")
    
    if y_mg > threshold:
        tilt_status.append("FORWARD")
    elif y_mg < -threshold:
        tilt_status.append("BACKWARD")
    
    if z_mg > 1200:  # Close to 1g when flat
        tilt_status.append("FLAT")
    elif z_mg < -1200:
        tilt_status.append("UPSIDE_DOWN")
    
    if tilt_status:
        print(f"Tilt: {', '.join(tilt_status)}")
    else:
        print("Tilt: NEUTRAL")

def test_different_ranges():
    """Test different acceleration ranges"""
    print("=== Testing Different Acceleration Ranges ===")
    
    # Initialize SPI
    spi = SPI(1, baudrate=1000000, polarity=0, phase=0, 
             sck=Pin(SCK_PIN), mosi=Pin(MOSI_PIN), miso=Pin(MISO_PIN))
    cs_pin = Pin(CS_PIN, Pin.OUT)
    
    accel_sensor = BMA250()
    
    ranges = [
        (BMA250.RANGE_2G, "2G"),
        (BMA250.RANGE_4G, "4G"), 
        (BMA250.RANGE_8G, "8G"),
        (BMA250.RANGE_16G, "16G")
    ]
    
    for range_val, range_name in ranges:
        print(f"\nTesting {range_name} range...")
        
        if accel_sensor.begin_spi(spi, cs_pin, range_val, BMA250.UPDATE_TIME_64MS):
            time.sleep(0.1)  # Allow sensor to settle
            accel_sensor.read()
            x_mg, y_mg, z_mg = accel_sensor.get_acceleration_mg(range_val)
            print(f"  Raw: X={accel_sensor.x}, Y={accel_sensor.y}, Z={accel_sensor.z}")
            print(f"  mg:  X={x_mg:.1f}, Y={y_mg:.1f}, Z={z_mg:.1f}")
        else:
            print(f"  Failed to initialize with {range_name} range")

if __name__ == "__main__":
    main()
    
    # Uncomment the line below to test different ranges
    # test_different_ranges()
