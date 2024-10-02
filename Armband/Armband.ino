#include <Arduino.h>
#include <BluetoothSerial.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  String SensorData = String("4096,4096,4096,4096,4096,4096,4096,4096.");
  
  Serial.print(SensorData);
  
  delay(10);
}
