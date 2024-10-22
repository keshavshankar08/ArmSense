import sys
sys.path.append('.')

import serial, threading, time, logging
from collections import deque
import numpy as np

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

    def connect(self, port, baud_rate):
        """
        Connects to the serial port.
        """
        try:
            self.device = serial.Serial(port, baud_rate, timeout=1)
            logging.info(f"Connected to serial port {port} at {baud_rate} baud.")
        except serial.SerialException as e:
            logging.error(f"Failed to connect to serial port {port}: {e}")
            raise e
        
    def disconnect(self):
        """
        Disconnects from the serial port.
        """
        if self.device:
            self.device.close()
            logging.info("Disconnected from serial port.")
        else:
            logging.warning("No serial port to disconnect from.")

    def start_reception(self, sampling_rate):
        """
        Starts the signal reception thread.
        """
        self.running = True
        self.thread = threading.Thread(target=self.receive_signals, args=(sampling_rate,), daemon=True)
        self.thread.start()  
        logging.info("SignalReceiver thread started.")

    def stop_reception(self):
        """
        Stops the signal reception thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        self.device.close()
        logging.info("SignalReceiver thread stopped and serial port closed.")

    def receive_signals(self, sampling_rate):
        """
        Continuously reads signals from the serial port at the specified rate.
        """
        read_interval = 1.0 / sampling_rate

        while self.running:
            start_time = time.time()
            try:
                line = self.device.read_until(b'.').decode('utf-8').strip('.')
                if line:
                    parts = line.split('.')[0].split(',')
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
