import Backend.feature_extractor as fe
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

        self.feature_extractor = fe.FeatureExtractor()
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None
        self.feature_data_file_name = "Hand/Backend/Resources/feature_data.csv"
        self.data_file_name = "Hand/Backend/Resources/data.csv"
        self.sampling_rate = 100
        self.window_size = 0.2
        self.interval_size = 0.05
        self.max_recording_time = 20
        self.feature_buffer = deque(maxlen=self.window_size * self.sampling_rate * self.max_recording_time)
        self.data_buffer = deque(maxlen=self.sampling_rate * self.max_recording_time)

    def start_collection(self, gesture_class):
        """
        Starts the data collection thread.

        :param gesture_class: The class of the gesture to be collected.
        """
        self.running = True
        self.thread = threading.Thread(target=self.collect_data, args=(gesture_class,), daemon=True)
        self.thread.start()

    def stop_collection(self):
        """
        Stops the data collection thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()
        self.save_data()

    def collect_data(self, gesture_class):
        '''
        Collects data for the given gesture class.

        :param gesture_class: The class of the gesture to be collected.
        '''
        with self.buffer_lock:
            self.feature_buffer.clear()
            self.data_buffer.clear()
            
        start_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if (elapsed_time >= self.interval_size):
                window = self.signal_receiver.get_last_n_signals(int(self.window_size * self.sampling_rate))
                features = self.feature_extractor.extract_features(window)
                features = np.append(features, gesture_class)
                data = np.append(window, gesture_class)
                with self.buffer_lock:
                    self.feature_buffer.append(features)
                    self.data_buffer.append(data)
                start_time = current_time

    def save_data(self):
        '''
        Saves the collected data to a file.

        :param output_data_file_name: The name of the file to save the collected data.
        '''
        with self.buffer_lock:
            try:
                with open(self.feature_data_file_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while self.feature_buffer:
                        writer.writerow(self.feature_buffer.popleft())
                with open(self.data_file_name, mode='a', newline='') as file:
                    writer = csv.writer(file)
                    while self.data_buffer:
                        writer.writerow(self.data_buffer.popleft())
            except Exception as e:
                return
            
    def clear_data(self):
        '''
        Clears the data set collection files.
        '''
        try:
            with open(self.feature_data_file_name, 'w') as file:
                file.truncate(0)
        except Exception as e:
            return