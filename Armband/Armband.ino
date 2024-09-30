#include <Arduino.h>
#include <BluetoothSerial.h>

void setup() {
  Serial.begin(115200);
}

void loop() {
  String SensorData = String("0,0,0,0,0,0,0,0.");
  
  Serial.println(SensorData);
  
  delay(2);
}
