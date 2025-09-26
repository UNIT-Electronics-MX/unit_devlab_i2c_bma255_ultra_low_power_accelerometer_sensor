# Hardware

<div align="center">
<a href="./unit_sch_v_1_0_0_ue0109_bma255_accelerometer_module.pdf"><img src="resources/Schematics_icon.jpg?raw=false" width="200px"><br/>Schematic</a>
</div>

## 🔌 Pinout

<div align="center">
    <a href="#"><img src="resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg" width="500px"><br/>Pinout</a>
    <br/>
    <br/>
    <br/>
    

| Pin Label | Function    | Notes                             |
|-----------|-------------|-----------------------------------|
| VCC       | Power Supply| 3.3V or 5V                       |
| GND       | Ground      | Common ground for all components  |

</div>

## 📏 Dimensions

<div align="center">
<a href="./resources/unit_dimension_v_1_0_0_ue0109_bma255_accelerometer_module.png"><img src="./resources/unit_dimension_v_1_0_0_ue0109_bma255_accelerometer_module.png" width="500px"><br/> Dimensions</a>
</div>

## 📃 Topology

<div align="center">

<div align="center">
<a href="./resources/unit_topology_v_1_0_0_ue0109_bma255_accelerometer_module.png"><img src="./resources/unit_topology_v_1_0_0_ue0109_bma255_accelerometer_module.png" width="500px"><br/> Topology</a>
<br/>
<br/>
<br/>

| Ref. | Description                              |
|------|------------------------------------------|
| IC1  | BMA255                                   |
| L1   | Power On LED                             |
| U1   | AP2112K 3V3 Regulator                    | 
| JP1  | 2.54 mm Castellated Holes                |
| J1   | QWIIC Connector (JST 1 mm pitch) for I2C |
| J2   | QWIIC Connector (JST 1 mm pitch) for I2C |
| J3   | JST 1 mm pitch for SPI                   |
| SW1  | Dip Switch for Mode Selection            |
| SB1  | Solder Bridge for I2C Pull-Ups           |
| SB2  | Solder Bridge for I2C Pull-Ups           |
| SB3  | Solder Bridge for I2C Address            |

</div>

## Pin & Connector Layout
| Pin   | Voltage Level | Function                                                  |
|-------|---------------|-----------------------------------------------------------|
| VCC   | 3.3 V – 5.5 V | Provides power to the on-board regulator and sensor core. |
| GND   | 0 V           | Common reference for power and signals.                   |
| SDA   | 1.8 V to VCC  | Serial data line for I²C communications.                  |
| SCL   | 1.8 V to VCC  | Serial clock line for I²C communications.                 |

> **Note:** The module also includes a Qwiic/STEMMA QT connector carrying the same four signals (VCC, GND, SDA, SCL) for effortless daisy-chaining.

## Functional Description

{{functional_description}}

## Applications

{{applications_list}}

# References

- [{{datasheet_name}}]({{datasheet_url}})
