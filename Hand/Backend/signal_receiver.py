import serial, threading, time, logging
from collections import deque
import numpy as np

from bleak import BleakClient
import asyncio

# logging.basicConfig(level=logging.DEBUG)

class SignalReceiver:
    def __init__(self, sampling_rate):
        """
        Initializes the SignalReceiver.

        :param sampling_rate: Sampling rate in Hz
        """
        self.sampling_rate = sampling_rate

        # self.port = '/dev/tty.usbserial-0001'
        # self.baud_rate = 115200
        # self.device = None
        self.signal_buffer = deque(maxlen=1000)
        self.buffer_lock = threading.Lock()
        self.keep_recieve_running = False  
        self.thread = None

        # Setup bluetooth
         # None uses default/autodetection, insert values if needed
        self.ADAPTER = None
        self.SERVICE_UUID = None
        self.WRITE_UUID = None
        self.READ_UUID = None
        self.DEVICE = "D8:13:2A:7F:2F:FE"
        # self.DEVICE = "08:A6:F7:BC:8F:62"

        # Characteristic UUID for communication (you need the correct one for your device)
        self.READ_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

        self.ble = BleakClient(self.DEVICE)

    def find_devices(self):
        # TODO: find devices to connect to
        pass

    async def connect(self):
        """
        Connects to the BLE serial port.
        """
        try:
            await self.ble.connect()
            print(f"Connected to {self.DEVICE}")
        except Exception as e:
            print(f"Failed to connect: {e}")

    async def start_reception(self):
        """
        Starts the signal reception thread.
        """
        # TODO: fix the issue with it never stopping the connection
        self.keep_recieve_running = True
        if self.ble.is_connected():
            print("Trying to get data from BLE")
            try:
                # Start receiving notifications
                await self.ble.start_notify(self.READ_UUID, self.receive_signals)

                # Keep the program running to continuously receive data
                while self.keep_recieve_running:
                    await asyncio.sleep(0.001)  # Adjust the time as needed

                # Stop receiving notifications
                await self.ble.stop_notify(self.READ_UUID)

            except Exception as e:
                logging.error(f"Failed to connect to bluetooth: {e}")

    def stop_reception(self):
        """
        Stops the signal reception thread.
        """
        # TODO: this does not work right now, connection is never stopped

        self.keep_recieve_running = False

    def receive_signals(self, sender, data):
        """
        Continuously reads signals from the serial port at the specified rate.
        """
        read_interval = 1.0 / self.sampling_rate

        while self.keep_recieve_running:
            start_time = time.time()
            try:
                line = data.decode('utf-8').strip('.').rstrip(',')
                print(line)
                if line:
                    parts = line.split('.')[0].split(',')
                    # print(parts)
                    if len(parts) != 8:
                        logging.warning(f"Incorrect data form received: {line}")
                        continue
                    try:
                        signal = [int(part) for part in parts]
                    except ValueError:
                        logging.warning(f"Non-integer value encountered in data: {line}")
                        continue

                    with self.buffer_lock:
                        self.signal_buffer.append(signal)
                    logging.debug(f"Received signal: {signal}")
                    logging.debug(f"Last added item in buffer: {self.signal_buffer[-1]}")
                    logging.debug(f"Buffer Length: {len(self.signal_buffer)}")
            except Exception as e:
                logging.error(f"Error receiving signals: {e}")

            elapsed_time = time.time() - start_time
            sleep_time = read_interval - elapsed_time
            if sleep_time > 0:
                time.sleep(sleep_time)
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
            