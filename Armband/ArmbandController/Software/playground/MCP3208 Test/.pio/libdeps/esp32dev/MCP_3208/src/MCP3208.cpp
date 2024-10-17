#include "MCP3208.h"

MCP3208::MCP3208() {}

void MCP3208::begin(uint8_t cs, SPIClass &spi) {
	this->cs = cs;
	pinMode(cs, OUTPUT);
	digitalWrite(cs, HIGH);
	this->spi = &spi;
	this->spi->begin();
	}

void MCP3208::analogReadResolution(uint8_t bits) {
	if (bits <=12 && bits >= 1)
		this->bits = bits;
	else this->bits = 10;
	}

uint16_t MCP3208::analogRead(uint8_t channel) {
	uint8_t addr = 0b01100000 | ((channel & 0b111) << 2);
	digitalWrite(cs, LOW);
	spi->transfer(addr);
	uint8_t byte1 = spi->transfer(0x00);
	uint8_t byte2 = spi->transfer(0x00);
	digitalWrite(cs, HIGH);
	return ((byte1 << 4) | (byte2 >> 4)) >> (RESOLUTION_MCP320X - bits);
	}