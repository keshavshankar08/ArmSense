# MCP3208 ADC Arduino library

Arduino library for Microchip MCP3208 A/D converter using SPI.<br>

## Example
Here is a simple example which shows the capabilities of the library

```cpp
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
```

# Documentation

## Constructor
```cpp
MCP3208();
```

Create an ADC.

**Example**

```cpp
MCP3208 adc;
```

## Methods

### **begin()**

```cpp
void begin(uint8_t cs = 10, SPIClass &spi = SPI);
```

- **cs** pin for chip select
- **spi** set optional SPI class to use (SPI, SPI1, SPI2 ...)

Initialize the SPI communication of the A/D converter.<br>
This must done in ```setup()```

**Example**

```cpp
setup() {
  adc.begin(); // SPI0, CS pin 10 (default)
  adc.begin(13, SPI1); // SPI1, CS pin 13
  }
```

### **analogReadResolution()**

Set the digital output resolution of the A/D converter.

```cpp
void analogReadResolution(uint8_t bits = 10);
```

- **bits** analog resolution (1 ... 12), default 10 bit

**Example**

```cpp
adc.analogReadResolution(12); // set resolution to 12 bit
```

### **analogRead()**

Read a single analog input.

```cpp
uint16_t analogRead(uint8_t channel);
```

- **channel** analog input (0 ... 7) to read

**Example**

```cpp
uint16_t channel0 = adc.analogRead(0);
```
