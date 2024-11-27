import threading, time
from collections import deque
import numpy as np
from bleak import BleakClient, BleakScanner
import asyncio

class SignalReceiver:
    def __init__(self):
        """
        Initializes the SignalReceiver.
        """
        self.signal_buffer = deque(maxlen=1000)
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

        self.device_name = "MDT UART Service"
        self.bt_address = ""
        self.CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
        self.client = BleakClient(self.bt_address)
        self.isBTRequested = False
        self.devices = None
        self.sampling_rate = 100

    def start_reception(self):
        """
        Starts the signal reception thread.
        """
        self.isBTRequested = True
        self.running = True
        self.thread = threading.Thread(target=self.run_async_receiver, daemon=True)
        self.thread.start()
            
    def stop_reception(self):
        """
        Stops the signal reception thread.
        """
        self.isBTRequested = False
        self.running = False
        if self.thread:
            self.thread.join()

    def run_async_receiver(self):
        """
        Runs the async bluetooth_receiver function in an event loop.
        """
        asyncio.run(self.bluetooth_receiver())

    async def bluetooth_receiver(self):
        async with BleakClient(self.bt_address) as client:
            if client.is_connected:
                print(f"Connected to {self.bt_address}")
                await client.start_notify(self.CHARACTERISTIC_UUID, self.receive_signals)

            while client.is_connected:
                await asyncio.sleep(0.0001)

                if not self.isBTRequested:
                    await client.stop_notify(self.CHARACTERISTIC_UUID)
                    await client.disconnect()
                        
    def receive_signals(self, _, data):
        """
        Continuously reads signals from the device.
        """
        read_interval = 1.0 / 1000

        if self.running:
            start_time = time.time()
            try:
                line = data.decode('utf-8').strip('.').rstrip(',')
                if line:
                    parts = line.split('.')[0].split(',')
                    if len(parts) != 8:
                        return

                    try:
                        signal = [int(part) for part in parts]
                    except ValueError:
                        return

                    if None not in signal:
                        with self.buffer_lock:
                            self.signal_buffer.append(signal)
            
            except Exception:
                return

            elapsed_time = time.time() - start_time
            sleep_time = read_interval - elapsed_time
            if sleep_time > 0:
                pass

    def get_last_n_signals(self, n):
        """
        Retrieves the last 'n' signals from the buffer.

        :param n: Number of recent signals to retrieve.
        :return: List of the last 'n' signals or None if insufficient data.
        """
        #change back to >= n
        with self.buffer_lock:
            if len(self.signal_buffer):
                return np.array(list(self.signal_buffer)[-n:])
            else:
                return None
            
    async def find_devices(self):
        """
        Scans for Bluetooth devices and stores the names and addresses of those called "MDT UART Service" in a list.
        """
        devices = await BleakScanner.discover()
        #self.devices = [(device.name, device.address) for device in devices if device.name and device.name[:-1] == self.device_name]
        self.devices = [(device.name, device.address) for device in devices if device.name and device.name == self.device_name]

    async def set_device(self, device_name):
        """
        Sets the Bluetooth address based on the device name.

        :param device_name: The name of the device to connect to.
        """
        for name, address in self.devices:
            if name == device_name:
                self.bt_address = address
                return
