import sys
sys.path.append('.')

from Hand.Backend.feature_extractor import *

import tensorflow as tf
import time, logging, threading
import csv

class Predictor:
    def __init__(self, signal_receiver):
        """
        Initializes the Predictor object.

        :param signal_receiver: The SignalReceiver object to receive signals from.
        """
        self.signal_receiver = signal_receiver

        self.feature_extractor = FeatureExtractor()
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None


    def start_prediction(self, model_file_name, min_vals, max_vals, sampling_rate, window_size, interval_size):
        """
        Starts the prediction thread.

        :param model: The trained model to be used for prediction.
        :param min_vals: The minimum values of the features for normalization.
        :param max_vals: The maximum values of the features for normalization.
        :param sampling_rate: The sampling rate of the signal receiver.
        :param window_size: The size of the window to be collected.
        :param interval_size: The interval size between each collection
        """
        self.running = True
        self.thread = threading.Thread(target=self.predict, args=(model_file_name, min_vals, max_vals, sampling_rate, window_size, interval_size,), daemon=True)
        self.thread.start()
        logging.info("Predictor thread started.")

    def stop_prediction(self):
        """
        Stops the prediction thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()

    def predict(self, model_file_name, min_vals, max_vals, sampling_rate, window_size, interval_size):
        """
        Predicts the gesture using the trained model.

        :param model_file_name: The file name of the trained model.
        :param min_vals: The minimum values of the features for normalization.
        :param max_vals: The maximum values of the features for normalization.
        :param sampling_rate: The sampling rate of the signal receiver.
        :param window_size: The size of the window to be collected.
        :param interval_size: The interval size between each collection
        """
        model = tf.keras.models.load_model(model_file_name)
        start_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if elapsed_time >= interval_size:
                window = self.signal_receiver.get_last_n_signals(int(window_size * sampling_rate))
                features = self.feature_extractor.extract_features(window)
                normalized_features = (features - min_vals) / (max_vals - min_vals)
                normalized_features = normalized_features.reshape(1, -1)
                predictions = model.predict(normalized_features)
                
                print("Predictions:", predictions)
                
                start_time = current_time

        
