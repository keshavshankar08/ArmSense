from Hand.Backend.feature_extractor import *

from collections import deque
import time, logging, threading
import numpy as np
import csv

class DataCollector:
    def __init__(self, signal_receiver, sampling_rate, window_size, interval_size, recording_size=3):
        self.signal_receiver = signal_receiver
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        self.interval_size = interval_size
        self.recording_size = recording_size

        self.file_name = "data.csv"
        self.feature_extractor = FeatureExtractor(self.sampling_rate)
        self.feature_buffer = deque(maxlen=int(3/self.interval_size))
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

    def start_collection(self, gesture_class):
        """
        Starts the data collection thread.
        """
        self.running = True
        self.thread = threading.Thread(target=self.collect_data, args=(gesture_class,), daemon=True)
        self.thread.start()
        logging.info("DataCollector thread started.")

    def stop_collection(self):
        """
        Stops the data collection thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        self.save_data()

    def collect_data(self, gesture_class):
        start_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if (elapsed_time >= self.interval_size):
                window = self.signal_receiver.get_last_n_signals(int(self.window_size * self.sampling_rate))
                features = self.feature_extractor.extract_features(window)
                features = np.append(features, gesture_class)
                with self.buffer_lock:
                    self.feature_buffer.append(features)
                start_time = current_time

    def save_data(self):
        with self.buffer_lock:
            with open(self.file_name, mode='a', newline='') as file:
                writer = csv.writer(file)
                while self.feature_buffer:
                    writer.writerow(self.feature_buffer.popleft())