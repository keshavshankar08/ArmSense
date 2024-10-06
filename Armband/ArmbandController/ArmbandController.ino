#include <Arduino.h>
#include <BluetoothSerial.h>

const int numChannels = 8;
const int signalDuration = 1000;
const int noiseLevel = 50;

unsigned long lastToggleTime = 0;
bool signalOn = false;

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long currentTime = millis();
  
  if (currentTime - lastToggleTime >= signalDuration) {
    signalOn = !signalOn;
    lastToggleTime = currentTime;
  }

  String SensorData = "";
  for (int i = 0; i < numChannels; i++) {
    int signalValue = signalOn ? random(2000, 4096) : random(0, 1000); // Simulate signal with noise
    SensorData += String(signalValue);
    if (i < numChannels - 1) {
      SensorData += ",";
    }
  }
  SensorData += ".";

  Serial.print(SensorData);
  delay(10);
}
