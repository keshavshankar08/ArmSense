#include <Arduino.h>

#include "MCP3208.h"
#include "string.h"

#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

BLEServer *pServer = NULL;
BLECharacteristic *pTxCharacteristic;
bool deviceConnected = false;
bool oldDeviceConnected = false;
uint8_t txValue = 0;

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"  // UART service UUID
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

MCP3208 adc;

int count = 0;

//Callback for the bluetooth server. 
class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer) {
    deviceConnected = true;
  };

  void onDisconnect(BLEServer *pServer) {
    deviceConnected = false;
  }
};

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  //============================== BLUETOOTH SETUP ==============================
  // Create the BLE Device
  BLEDevice::init("UART Service");

  // Create the BLE Server
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks()); 

  // Create the BLE Service
  BLEService *pService = pServer->createService(SERVICE_UUID);

  // Create a BLE Characteristic
  pTxCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY);

  pTxCharacteristic->addDescriptor(new BLE2902());

  // Start the service
  pService->start();

  // Start advertising
  pServer->getAdvertising()->start();
  Serial.println("Waiting a client connection to notify...");
  //=============================================================================



  /// Hardware SPI (specify CS, use any available digital pin)
  /// Can use defaults if available, 
  /// ex: UNO (SS=10), Huzzah (SS=15), Feather 32u4 (SS=17) or M0 (SS=16)
  adc.begin(5);
  adc.analogReadResolution(12);
}

void loop() {
  // put your main code here, to run repeatedly:

  // get ADC data and concatnate to string 
  String test = "";
  for (int chan=0; chan<8; chan++) {
    Serial.print(adc.analogRead(chan)); Serial.print("\t");
    test += String(adc.analogRead(chan));
    test += ",";
  }
  test += ".";

  Serial.print("["); Serial.print(count); Serial.println("]");
  count++;

  //================Bluetooth Code==================
  std::string payload = test.c_str();
  // std::string payload = "Test";
  if (deviceConnected) {
    // pTxCharacteristic->setValue(&txValue, 0x56);
    pTxCharacteristic->setValue(payload);  //String value
    pTxCharacteristic->notify();
    txValue++;
    // delay(1);  // bluetooth stack will go into congestion, if too many packets are sent
  }

  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500);                   // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising();  // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }
  //================================================
  
  delay(1);
}