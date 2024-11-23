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

//=================================== PROTOTYPES ===============================
void getADCData();
void sendBTData();
//=================================== PROTOTYPES ===============================


//=================================== GLOBAL DEFS ==============================
#define INTERVAL 8
//=================================== GLOBAL DEFS ==============================

//=================================== GLOBAL VARS ==============================
int count = 0;
String adcData = "";
unsigned long previousTime = 0; 
bool transmitFailed = false;
//=================================== GLOBAL VARS ==============================


//Callback for the bluetooth server. 
class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer *pServer) {
    deviceConnected = true;
  };

  void onDisconnect(BLEServer *pServer) {
    deviceConnected = false;
  }
};

void gattsEventCallback(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t* param) {
    if (event == ESP_GATTS_CONF_EVT) {
        if (param->conf.status != ESP_GATT_OK) {
          Serial.printf("Notification failed with status: %d\n", param->conf.status);
          transmitFailed = true;
        }
        else if (param->conf.status == ESP_GATT_OK)
        {
          transmitFailed = false;
        }
    }
}

//============================== FastLED Definitions ==============================
#define NUM_LEDS 1
#define DATA_PIN 26
CRGB leds[NUM_LEDS];
//========================== End FastLED Definitions ==============================

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  while (!Serial);

  //============================== Debug LED SETUP ==============================
  FastLED.addLeds<WS2812B, DATA_PIN, GRB>(leds, NUM_LEDS);  
  leds[0] = CRGB::Black;
  FastLED.setBrightness(50);
  FastLED.show();
  Serial.println("Firmware Version: 0.1");
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
}

void loop() {
  // put your main code here, to run repeatedly:
  // leds[0] = CRGB::Black;  //Loop Blink
  // FastLED.show();

  unsigned long currentTime = millis();

  if(currentTime-previousTime>INTERVAL)
  {
    //Get ADC Data
    getADCData();
    //================Bluetooth Code==================
    sendBTData();
    //================================================

    if(!transmitFailed)
    {
      previousTime = currentTime;
    }
  }
}

void getADCData()
{
  // get ADC data and concatnate to string 
  adcData = "";
  for (int chan=0; chan<8; chan++) {
    adcData += String(adc.analogRead(chan));
    adcData += ",";
  }
  adcData += ".";

  // Serial.print("["); Serial.print(count); Serial.println("]");
}

void sendBTData()
{
    std::string payload = adcData.c_str();
  // std::string payload = "Test";
  if (deviceConnected) {
    // pTxCharacteristic->setValue(&txValue, 0x56);
    pTxCharacteristic->setValue(payload);  //String value
    pTxCharacteristic->notify();
    txValue++;

    leds[0] = CRGB::Green;  //Running BT 
    FastLED.show();
    // delay(1);  // bluetooth stack will go into congestion, if too many packets are sent
  }
  else
  {
    leds[0] = CRGB::DarkRed;  //Running BT 
    FastLED.show();
  }

  // disconnecting
  if (!deviceConnected && oldDeviceConnected) {
    delay(500);                   // give the bluetooth stack the chance to get things ready
    pServer->startAdvertising();  // restart advertising
    Serial.println("start advertising");
    oldDeviceConnected = deviceConnected;

    leds[0] = CRGB::Red;  //ADC Setup
    FastLED.show();
  }
  // connecting
  if (deviceConnected && !oldDeviceConnected) {
    // do stuff here on connecting
    oldDeviceConnected = deviceConnected;
  }
}