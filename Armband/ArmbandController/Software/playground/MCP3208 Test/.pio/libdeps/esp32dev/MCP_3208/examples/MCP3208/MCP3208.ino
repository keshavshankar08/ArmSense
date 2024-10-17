#include "MCP3208.h"

MCP3208 adc;

uint16_t channel0;
uint16_t channel1;

void setup() {
	Serial.begin(9600);
	adc.begin(); // default pin 10 for CS; pin 17 for Pico on SPI0
	adc.analogReadResolution(12); // set resolution to 12 bit instead 10 bit (default)
	}

void loop() {
	channel0 = adc.analogRead(0);
	channel1 = adc.analogRead(1);
	Serial.print("Channel 0 Value: ");
	Serial.println(channel0);
	Serial.print("Channel 1 Value: ");
	Serial.println(channel1);
	delay(500);
	}