from Hand.Backend.feature_extractor import *

import tensorflow as tf
import time, logging, threading
import csv

class Predictor:
    def __init__(self, signal_receiver, sampling_rate, window_size, interval_size):
        self.signal_receiver = signal_receiver
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        self.interval_size = interval_size

        self.model = tf.keras.models.load_model("model.h5")
        self.feature_extractor = FeatureExtractor(self.sampling_rate)
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

        with open('vars.csv', mode='r') as file:
            reader = csv.reader(file)
            self.min_vals = np.array(next(reader), dtype=float)
            self.max_vals = np.array(next(reader), dtype=float)

    def start_prediction(self):
        """
        Starts the prediction thread.
        """
        self.running = True
        self.thread = threading.Thread(target=self.collect_data, daemon=True)
        self.thread.start()
        logging.info("Predictor thread started.")

    def stop_prediction(self):
        """
        Stops the prediction thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()

    def predict(self):
        start_time = time.time()

        while self.running:
            current_time = time.time()
            elapsed_time = current_time - start_time

            if (elapsed_time >= self.interval_size):
                window = self.signal_receiver.get_last_n_signals(int(self.window_size * self.sampling_rate))
                features = self.feature_extractor.extract_features(window)
                if not any(tf.math.is_nan(features).numpy()):
                    features = np.array(features, dtype=float)
                    normalized_features = (features - self.min_vals) / (self.max_vals - self.min_vals)
                    prediction = self.model.predict(tf.expand_dims(normalized_features, axis=0))
                    print(f"Prediction: {prediction}")
                else:
                    logging.warning("NaN values found in features, skipping prediction.")
                start_time = current_time

        
