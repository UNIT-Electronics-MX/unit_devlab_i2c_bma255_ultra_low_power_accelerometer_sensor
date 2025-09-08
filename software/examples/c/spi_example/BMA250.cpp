#include "BMA250.h"
#include <inttypes.h>
#include "Arduino.h"

BMA250::BMA250()
{
    _mode = BMA250_MODE_I2C;
    _cs_pin = 0;
    _spi = nullptr;
    _spi_frequency = 1000000; // 1MHz default
    I2Caddress = 0;
}

// Legacy I2C initialization (for backward compatibility)
int BMA250::begin(uint8_t range, uint8_t bw)
{
    return beginI2C(range, bw);
}

// I2C initialization
int BMA250::beginI2C(uint8_t range, uint8_t bw, uint8_t i2c_addr)
{
    _mode = BMA250_MODE_I2C;
    
    // Detect I2C address
    I2Caddress = i2c_addr;
    Wire.beginTransmission(I2Caddress);
    if (Wire.endTransmission()) {
        I2Caddress++;
        Wire.beginTransmission(I2Caddress);
        if (Wire.endTransmission()) {
            I2Caddress = 0;
            return -1;
        }
    }
    
    // Setup the range measurement setting
    writeRegister(BMA250_REG_RANGE, range);
    
    // Setup the bandwidth
    writeRegister(BMA250_REG_BW, bw);
    
    return 0;
}

// SPI initialization
int BMA250::beginSPI(uint8_t range, uint8_t bw, uint8_t cs_pin, SPIClass* spi_instance)
{
    _mode = BMA250_MODE_SPI;
    _cs_pin = cs_pin;
    _spi = spi_instance;
    
    // Configure CS pin
    pinMode(_cs_pin, OUTPUT);
    digitalWrite(_cs_pin, HIGH);
    
    // Initialize SPI
    _spi->begin();
    
    // Try to read chip ID to verify communication
    uint8_t chipId = readRegister(BMA250_REG_CHIPID);
    if (chipId == 0x00 || chipId == 0xFF) {
        return -1; // Communication failed
    }
    
    // Setup the range measurement setting
    writeRegister(BMA250_REG_RANGE, range);
    
    // Setup the bandwidth
    writeRegister(BMA250_REG_BW, bw);
    
    return 0;
}

void BMA250::read()
{
    if (_mode == BMA250_MODE_I2C) {
        // I2C read implementation
        Wire.beginTransmission(I2Caddress);
        Wire.write(BMA250_REG_X_LSB);
        Wire.endTransmission();
        
        Wire.requestFrom(I2Caddress, 7);
        
        X = (int16_t)Wire.read();
        X |= (int16_t)Wire.read() << 8;
        Y = (int16_t)Wire.read();
        Y |= (int16_t)Wire.read() << 8;
        Z = (int16_t)Wire.read();
        Z |= (int16_t)Wire.read() << 8;
        
        rawTemp = Wire.read();
    } else {
        // SPI read implementation
        uint8_t buffer[7];
        readMultipleRegisters(BMA250_REG_X_LSB, buffer, 7);
        
        X = (int16_t)buffer[0];
        X |= (int16_t)buffer[1] << 8;
        Y = (int16_t)buffer[2];
        Y |= (int16_t)buffer[3] << 8;
        Z = (int16_t)buffer[4];
        Z |= (int16_t)buffer[5] << 8;
        
        rawTemp = buffer[6];
    }
    
    // Only use the 10 significant bits
    X >>= 6; 
    Y >>= 6; 
    Z >>= 6;
    
    // Calculate temperature
    tempC = rawTemp/2 + 23;
}

void BMA250::writeRegister(uint8_t reg, uint8_t value)
{
    if (_mode == BMA250_MODE_I2C) {
        Wire.beginTransmission(I2Caddress);
        Wire.write(reg);
        Wire.write(value);
        Wire.endTransmission();
    } else {
        spiBeginTransaction();
        digitalWrite(_cs_pin, LOW);
        _spi->transfer(reg | BMA250_SPI_WRITE);
        _spi->transfer(value);
        digitalWrite(_cs_pin, HIGH);
        spiEndTransaction();
    }
}

uint8_t BMA250::readRegister(uint8_t reg)
{
    uint8_t value = 0;
    
    if (_mode == BMA250_MODE_I2C) {
        Wire.beginTransmission(I2Caddress);
        Wire.write(reg);
        Wire.endTransmission();
        Wire.requestFrom(I2Caddress, 1);
        if (Wire.available()) {
            value = Wire.read();
        }
    } else {
        spiBeginTransaction();
        digitalWrite(_cs_pin, LOW);
        _spi->transfer(reg | BMA250_SPI_READ);
        value = _spi->transfer(0x00);
        digitalWrite(_cs_pin, HIGH);
        spiEndTransaction();
    }
    
    return value;
}

void BMA250::readMultipleRegisters(uint8_t reg, uint8_t* buffer, uint8_t length)
{
    if (_mode == BMA250_MODE_I2C) {
        Wire.beginTransmission(I2Caddress);
        Wire.write(reg);
        Wire.endTransmission();
        Wire.requestFrom(I2Caddress, length);
        
        for (uint8_t i = 0; i < length; i++) {
            if (Wire.available()) {
                buffer[i] = Wire.read();
            } else {
                buffer[i] = 0;
            }
        }
    } else {
        spiBeginTransaction();
        for (uint8_t i = 0; i < length; i++) {
            digitalWrite(_cs_pin, LOW);
            _spi->transfer((reg + i) | BMA250_SPI_READ);
            buffer[i] = _spi->transfer(0x00);
            digitalWrite(_cs_pin, HIGH);
            delayMicroseconds(1);
        }
        spiEndTransaction();
    }
}

void BMA250::spiBeginTransaction()
{
    _spi->beginTransaction(SPISettings(_spi_frequency, MSBFIRST, SPI_MODE0));
}

void BMA250::spiEndTransaction()
{
    _spi->endTransaction();
}
