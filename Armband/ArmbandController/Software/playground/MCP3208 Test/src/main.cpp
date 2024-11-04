#include <Arduino.h>

#include "MCP3208.h"

MCP3208 adc;

int count = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  Serial.println("MCP3208 simple test.");

  /// Hardware SPI (specify CS, use any available digital pin)
  /// Can use defaults if available, 
  /// ex: UNO (SS=10), Huzzah (SS=15), Feather 32u4 (SS=17) or M0 (SS=16)
  adc.begin(5);
  adc.analogReadResolution(12);
}

void loop() {
  // put your main code here, to run repeatedly:
  for (int chan=0; chan<8; chan++) {
    Serial.print(adc.analogRead(chan)); Serial.print("\t");
  }

  Serial.print("["); Serial.print(count); Serial.println("]");
  count++;
  
  delay(1);
}