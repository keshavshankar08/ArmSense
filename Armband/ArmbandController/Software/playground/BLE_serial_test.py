import ble_serial
import time

class BLESerialReceiver:
    def __init__(self, device_address):
        self.device_address = device_address
        self.ble_serial = ble_serial.BLE_Serial(ble_serial.BLEDeviceInfo(device_address))

    def connect(self):
        self.ble_serial.connect()

    def receive_data(self):
        data = self.ble_serial.read()
        if data:
            print(f"Received: {data}")

    def disconnect(self):
        self.ble_serial.disconnect()

# Usage
device_address = "D8:13:2A:7F:2F:FE"  # Replace with your BLE device address
receiver = BLESerialReceiver(device_address)
receiver.connect()
receiver.receive_data()  # Continuously read from the BLE device
time.sleep(20)
receiver.disconnect()