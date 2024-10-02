#include <Arduino.h>
#include <BluetoothSerial.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  String SensorData = String("100,100,100,100,100,100,100,100.");
  
  Serial.print(SensorData);
  
  delay(10);
}
