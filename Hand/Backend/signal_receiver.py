import sys
sys.path.append('.')

import serial, threading, time, logging
from collections import deque
import numpy as np

# Bluetooth imports
from bleak import BleakClient
import asyncio

class SignalReceiver:
    def __init__(self):
        """
        Initializes the SignalReceiver.
        """
        self.device = None
        self.signal_buffer = deque(maxlen=1000)
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

        self.bt_address = "D8:13:2A:7F:2F:FE"
        self.CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
        self.client = BleakClient(self.bt_address)
        self.isBTRequested = False


    def connect(self):
        """
        Connects to the serial port.
        """
        self.isBTRequested = True
        self.running = True
        asyncio.run(self.start_bluetooth_recieve())
        
    def disconnect(self):
        """
        Disconnects from the serial port.
        """
        # TODO: Add safe close 
        self.isBTRequested = False

    def start_reception(self, sampling_rate):
        """
        Starts the signal reception thread.
        """
        #TODO: add a way to start BT connection but noot receive data
            


    def stop_reception(self):
        """
        Stops the signal reception thread.
        """
        #TODO: add a way to stop signal receive and keep the connection alive
        # logging.info("SignalReceiver thread stopped and serial port closed.")

    def receive_signals(self, sender, data):
        """
        Continuously reads signals from the serial port at the specified rate.
        """
        read_interval = 1.0 / 1000

        if self.running:
            start_time = time.time()
            try:
                line = data.decode('utf-8').strip('.').rstrip(',')
                if line:
                    parts = line.split('.')[0].split(',')
                    if len(parts) != 8:
                        logging.warning(f"Incorrect data form received: {line}")

                    try:
                        signal = [int(part) for part in parts]
                    except ValueError:
                        logging.warning(f"Non-integer value encountered in data: {line}")

                    if None not in signal:
                        with self.buffer_lock:
                            self.signal_buffer.append(signal)
                    else:
                        logging.warning(f"Null value encountered in signal: {signal}")
                    logging.debug(f"Received signal: {signal}")
                    # print(f"Received signal: {signal}")
            except Exception as e:
                logging.error(f"Error receiving signals: {e}")

            elapsed_time = time.time() - start_time
            sleep_time = read_interval - elapsed_time
            if sleep_time > 0:
                # time.sleep(sleep_time)
                pass
            else:
                logging.warning("Signal reception is lagging behind the desired rate.")

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
            

    async def start_bluetooth_recieve(self):
        async with BleakClient(self.bt_address) as client:
            if client.is_connected:
                print(f"Connected to {self.bt_address}")
                logging.info(f"Connected to {self.bt_address}")
                await client.start_notify(self.CHARACTERISTIC_UUID, self.receive_signals)

            while client.is_connected:
                # Start receiving notifications
                # await client.start_notify(self.CHARACTERISTIC_UUID, self.receive_signals)

                # Keep the program running to continuously receive data
                await asyncio.sleep(0.0001)  # Adjust the time as needed

                # Stop receiving notifications
                # await client.stop_notify(self.CHARACTERISTIC_UUID)
