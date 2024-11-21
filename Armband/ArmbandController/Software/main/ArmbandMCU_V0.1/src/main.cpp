#include <Arduino.h>

#include <FastLED.h>

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


//=================================== GLOBAL VARS ==============================
String adcData = "";
//=================================== GLOBAL VARS ==============================

//============================== FastLED Definitions ==============================
#define NUM_LEDS 1
#define DATA_PIN 26
CRGB leds[NUM_LEDS];
//=============================================================================

//============================== RTOS BT Setup ==============================
//Send bluetooth data based on params passed in
void sendBluetoothData(void *param)
{
  for(;;)
  {
    String *data = (String*) param;
    std::string payload = data->c_str();
    if (deviceConnected) {
      pTxCharacteristic->setValue(payload);  //String value
      pTxCharacteristic->notify();
      // txValue++;
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

    vTaskDelay(7 / portTICK_PERIOD_MS);  // bluetooth stack will go into congestion, if too many packets are sent
  }

}
//============================== RTOS BT Setup ==============================


//============================== RTOS ADC Setup ==============================
//Send bluetooth data based on params passed in
void getADCData(void *param)
{
  for(;;)
  {
    // get ADC data and concatnate to string 
    adcData = "";
    for (int chan=0; chan<8; chan++) {
      // Serial.print(adc.analogRead(chan)); Serial.print("\t");
      adcData += String(adc.analogRead(chan));
      adcData += ",";
    }
    adcData += ".";

    vTaskDelay(10 / portTICK_PERIOD_MS);  // bluetooth stack will go into congestion, if too many packets are sent
  }

}
//============================== RTOS ADC Setup ==============================


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  //============================== Debug LED SETUP ==============================
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);  
  leds[0] = CRGB::Black;
  FastLED.setBrightness(50);
  FastLED.show();
  //=============================================================================

  //============================== BLUETOOTH SETUP ==============================
  // Create the BLE Device
  BLEDevice::init("ArmSense");

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

  leds[0] = CRGB::LightBlue;  //BT Setup
  FastLED.show();
  delay(100);
  //=============================================================================


  //=================================== ADC SETUP ==============================
  /// Hardware SPI (specify CS, use any available digital pin)
  /// Can use defaults if available, 
  /// ex: UNO (SS=10), Huzzah (SS=15), Feather 32u4 (SS=17) or M0 (SS=16)
  adc.begin(5);
  adc.analogReadResolution(12);
  leds[0] = CRGB::Navy;  //ADC Setup
  FastLED.show();
  delay(100);
  //=============================================================================

  // //=================================== FREERTOS SETUP BT ==============================
  // xTaskCreatePinnedToCore
  // (
  //   sendBluetoothData,
  //   "Send BT Data",
  //   4096,
  //   &adcData,
  //   1,
  //   NULL,
  //   0
  // );
  // //=================================== FREERTOS SETUP BT ==============================

  // //=================================== FREERTOS SETUP ADC ==============================
  // xTaskCreatePinnedToCore
  // (
  //   getADCData,
  //   "Send BT Data",
  //   8192,
  //   NULL,
  //   2,
  //   NULL,
  //   1
  // );
  // //=================================== FREERTOS SETUP ADC ==============================
    //=================================== FREERTOS SETUP BT ==============================
  xTaskCreate
  (
    sendBluetoothData,
    "Send BT Data",
    4096,
    &adcData,
    1,
    NULL
  );
  //=================================== FREERTOS SETUP BT ==============================

  //=================================== FREERTOS SETUP ADC ==============================
  xTaskCreate
  (
    getADCData,
    "Send BT Data",
    8192,
    NULL,
    2,
    NULL
  );
  //=================================== FREERTOS SETUP ADC ==============================
}

void loop() {
  // put your main code here, to run repeatedly:
  // leds[0] = CRGB::Black;  //Loop Blink
  // FastLED.show();

  //   // disconnecting
  // if (!deviceConnected && oldDeviceConnected) {
  //   delay(500);                   // give the bluetooth stack the chance to get things ready
  //   pServer->startAdvertising();  // restart advertising
  //   Serial.println("start advertising");
  //   oldDeviceConnected = deviceConnected;
  // }
  // // connecting
  // if (deviceConnected && !oldDeviceConnected) {
  //   // do stuff here on connecting
  //   oldDeviceConnected = deviceConnected;
  // }

  // // get ADC data and concatnate to string 
  // adcData = "";
  // for (int chan=0; chan<8; chan++) {
  //   // Serial.print(adc.analogRead(chan)); Serial.print("\t");
  //   adcData += String(adc.analogRead(chan));
  //   adcData += ",";
  // }
  // adcData += ".";

  // Serial.print("["); Serial.print(count); Serial.println("]");
  // count++;
  
  // delay(1);
}