#ifndef BMA250_h
#define BMA250_h

// I2C Configuration
#define BMA250_I2CADDR 0x18

// SPI Configuration
#define BMA250_SPI_READ 0x80
#define BMA250_SPI_WRITE 0x00

// Register definitions
#define BMA250_REG_CHIPID 0x00
#define BMA250_REG_RANGE 0x0F
#define BMA250_REG_BW 0x10
#define BMA250_REG_X_LSB 0x02
#define BMA250_REG_X_MSB 0x03
#define BMA250_REG_Y_LSB 0x04
#define BMA250_REG_Y_MSB 0x05
#define BMA250_REG_Z_LSB 0x06
#define BMA250_REG_Z_MSB 0x07
#define BMA250_REG_TEMP 0x08

// Update time settings
#define BMA250_update_time_64ms 0x08
#define BMA250_update_time_32ms 0x09
#define BMA250_update_time_16ms 0x0A
#define BMA250_update_time_8ms 0x0B
#define BMA250_update_time_4ms 0x0C
#define BMA250_update_time_2ms 0x0D
#define BMA250_update_time_1ms 0x0E
#define BMA250_update_time_05ms 0x0F

// Range settings
#define BMA250_range_2g 0x03
#define BMA250_range_4g 0x05
#define BMA250_range_8g 0x08
#define BMA250_range_16g 0x0C

// Communication modes
#define BMA250_MODE_I2C 0
#define BMA250_MODE_SPI 1

#include <inttypes.h>
#include <SPI.h>
#include <Wire.h>

class BMA250 {
public:
    BMA250();
    
    // I2C initialization
    int begin(uint8_t range, uint8_t bw);
    int beginI2C(uint8_t range, uint8_t bw, uint8_t i2c_addr = BMA250_I2CADDR);
    
    // SPI initialization
    int beginSPI(uint8_t range, uint8_t bw, uint8_t cs_pin, SPIClass* spi_instance = &SPI);
    
    // Data reading
    void read();
    
    // Public variables
    int16_t X, Y, Z;
    int8_t rawTemp;
    int8_t tempC;
    uint8_t I2Caddress = 0;
    
private:
    uint8_t _mode;           // Communication mode (I2C or SPI)
    uint8_t _cs_pin;         // SPI Chip Select pin
    SPIClass* _spi;          // SPI instance
    uint32_t _spi_frequency; // SPI frequency
    
    // Internal communication functions
    void writeRegister(uint8_t reg, uint8_t value);
    uint8_t readRegister(uint8_t reg);
    void readMultipleRegisters(uint8_t reg, uint8_t* buffer, uint8_t length);
    
    // SPI helper functions
    void spiBeginTransaction();
    void spiEndTransaction();
};

#endif
