/*
	SPI library for Microchip A/D converter MCP23017
	(c)sstaub 2023 under MIT license
*/

#ifndef MCP3208_H
#define MCP3208_H

#include "Arduino.h"
#include "SPI.h"

#define RESOLUTION_MCP320X 12

/**
 * @brief Class for MCP3208
 * 
 */
class MCP3208 {
	public:

		/**
		 * @brief Construct a new MCP3208 object
		 * 
		 */
		MCP3208();

		/**
		 * @brief Initializes the MCP3208
		 * 
		 * @param cs chip select pin
		 * @param spi alternatives SPI Ports, SPI and SPI1 ...
		 */
		void begin(uint8_t cs = 10, SPIClass &spi = SPI);

		/**
		 * @brief Set the resolution of the ADC
		 * 
		 * @param bits 
		 */
		void analogReadResolution(uint8_t bits = 10);

		/**
		 * @brief Get the channel value
		 * 
		 * @param channel 
		 * @return uint16_t value
		 */
		uint16_t analogRead(uint8_t channel);

	private:
		SPIClass *spi;
		uint8_t cs;
		uint8_t bits = 10;
	};

#endif