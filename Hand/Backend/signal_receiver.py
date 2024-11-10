import sys
sys.path.append('.')

import threading, time
from collections import deque
import numpy as np
from bleak import BleakClient
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

        self.bt_address = "76FF84F4-9D42-7F49-B6BB-F2EA5F824A8D"
        self.CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
        self.client = BleakClient(self.bt_address)
        self.isBTRequested = False

    def start_reception(self, sampling_rate):
        """
        Starts the signal reception thread.
        """
        self.isBTRequested = True
        self.running = True
        self.thread = threading.Thread(target=self.run_async_receiver, args=(sampling_rate,), daemon=True)
        self.thread.start()
            
    def stop_reception(self):
        """
        Stops the signal reception thread.
        """
        self.isBTRequested = False
        self.running = False
        if self.thread:
            self.thread.join()

    def run_async_receiver(self, sampling_rate):
        """
        Runs the async bluetooth_receiver function in an event loop.
        """
        asyncio.run(self.bluetooth_receiver(sampling_rate))

    async def bluetooth_receiver(self, _):
        async with BleakClient(self.bt_address) as client:
            if client.is_connected:
                print(f"Connected to {self.bt_address}")
                await client.start_notify(self.CHARACTERISTIC_UUID, self.receive_signals)

            while client.is_connected:
                # Keep the program running to continuously receive data
                await asyncio.sleep(0.0001)  # Adjust the time as needed

                # Stop receiving notifications
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
        with self.buffer_lock:
            if len(self.signal_buffer) >= n:
                return np.array(list(self.signal_buffer)[-n:])
            else:
                return None