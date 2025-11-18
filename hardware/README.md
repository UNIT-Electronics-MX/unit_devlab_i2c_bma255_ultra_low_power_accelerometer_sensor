# Hardware

<div align="center">
<a href="./unit_sch_v_1_0_0_ue0109_bma250_accelerometer_module.pdf"><img src="resources/Schematics_icon.jpg?raw=false" width="200px"><br/>Schematic</a>
</div>

## Technical Specifications

### Electrical Characteristics

<div align="center">

| **Parameter** |           **Description**            |  **Min**  | **Typ** |  **Max**  | **Unit** |
|:-------------:|:------------------------------------:|:---------:|:-------:|:---------:|:--------:|
|      Vin      | Input voltage to power on the module |    2.5    |    -    |    5.5    |    V     |
|      Vdd      |      Supply Voltage for sensor       |   1.62    |    -    |    3.6    |    V     |
|     Vddio     |        Supply Voltage for I/O        |    1.2    |   2.4   |    3.6    |    V     |
|      Idd      |         Total Supply Current         |    6.5    |    -    |    130    |    uA    |
|    I3v3(1)    |   Maximum current of 3V3 regulator   |     -     |    -    |    600    |    mA    |
|      Vih      |       Input high level voltage       | 0.7 Vddio |    -    |     -     |    V     |
|      Vil      |       Input low level voltage        |     -     |    -    | 0.3 Vddio |    V     |
|      Vol      |       Output low level voltage       |     -     |    -    | 0.2 Vddio |    V     |
|      Voh      |      Output high level voltage       | 0.8 Vddio |    -    |     -     |    V     |
|    Sxg(2)     |             Sensitivity              |    128    |    -    |   1024    |  LSB/g   |
|      Off      |            Zero-g Offset             |     -     |   ±60   |     -     |    mg    |
|    bwx(3)     |              Bandwidth               |     8     |    -    |   1000    |    Hz    |

</div>

(1) Optimal thermal management is required for the regulator to perform reliably at maximum output current.

(2)(3) To get more information about minimum and maximum values and how to configure, please refer to BMA255 manufacturer datasheet. 



## Pinout

<div align="center">
    <a href="#"><img src="resources/unit_pinout_v_0_0_1_ue0094_icp10111_barometric_pressure_sensor_en.jpg" width="500px"><br/>Pinout</a>
    <br/>
    <br/>
    <br/>

</div>    

### Pin & Connector Layout

<div align="center">

| Pin   | Voltage Level | Function                                                  |
|-------|---------------|-----------------------------------------------------------|
| VCC   | 3.3 V – 5.5 V | Provides power to the on-board regulator and sensor core. |
| GND   | 0 V           | Common reference for power and signals.                   |
| SDA   | 1.8 V to VCC  | Serial data line for I²C communications.                  |
| SCL   | 1.8 V to VCC  | Serial clock line for I²C communications.                 |

> **Note:** The module also includes a Qwiic/STEMMA QT connector carrying the same four signals (VCC, GND, SDA, SCL) for effortless daisy-chaining.

</div>

## Topology

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

## Dimensions

<div align="center">
<a href="./resources/unit_dimension_v_1_0_0_ue0109_bma255_accelerometer_module.png"><img src="./resources/unit_dimension_v_1_0_0_ue0109_bma255_accelerometer_module.png" width="500px"><br/> Dimensions</a>
</div>

# References

- <a href="./resources/unit_datasheet_v_1_0_0_ue0109_bma255_chip.pdf">BMA255 Datasheet</a>
