import sys
sys.path.append('.')

from Hand.Backend.feature_extractor import *

from collections import deque
import time, threading
import numpy as np
import csv

class DataCollector:
    def __init__(self, signal_receiver):
        """
        Initializes the DataCollector.

        :param signal_receiver: SignalReceiver instance
        """
        self.signal_receiver = signal_receiver

        self.feature_extractor = FeatureExtractor()
        self.feature_buffer = deque(maxlen=100)
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

    def start_collection(self, gesture_class, sampling_rate, window_size, interval_size):
        """
        Starts the data collection thread.

        :param gesture_class: The class of the gesture to be collected.
        :param sampling_rate: The sampling rate of the signal receiver.
        :param window_size: The size of the window to be collected.
        :param interval_size: The interval size between each collection
        """
        self.running = True
        self.thread = threading.Thread(target=self.collect_data, args=(gesture_class, sampling_rate, window_size, interval_size,), daemon=True)
        self.thread.start()

    def stop_collection(self, output_data_file_name):
        """
        Stops the data collection thread.

        :param output_data_file_name: The name of the file to save the collected data.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        self.save_data(output_data_file_name)

    def collect_data(self, gesture_class, sampling_rate, window_size, interval_size):
        '''
        Collects data for the given gesture class.

        :param gesture_class: The class of the gesture to be collected.
        :param sampling_rate: The sampling rate of the signal receiver.
        :param window_size: The size of the window to be collected.
        :param interval_size: The interval size between each collection
        '''
        start_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if (elapsed_time >= interval_size):
                window = self.signal_receiver.get_last_n_signals(int(window_size * sampling_rate))
                features = self.feature_extractor.extract_features(window)
                features = np.append(features, gesture_class)
                with self.buffer_lock:
                    self.feature_buffer.append(features)
                start_time = current_time

    def save_data(self, output_data_file_name):
        '''
        Saves the collected data to a file.

        :param output_data_file_name: The name of the file to save the collected data.
        '''
        with self.buffer_lock:
            try:
                with open(output_data_file_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while self.feature_buffer:
                        writer.writerow(self.feature_buffer.popleft())
            except Exception as e:
                return