import Hand.Backend.feature_extractor as fe
import csv
import tensorflow as tf
import time, threading
import numpy as np

class Predictor:
    def __init__(self, signal_receiver):
        """
        Initializes the Predictor object.

        :param signal_receiver: The SignalReceiver object to receive signals from.
        """
        self.signal_receiver = signal_receiver

        self.feature_extractor = fe.FeatureExtractor()
        self.buffer_lock = threading.Lock()
        self.running = False
        self.thread = None

        self.last_prediction = None
        self.last_error = None

        self.model_file_path = "Hand/Backend/Resources/model.h5"
        self.normalization_bounds_file_name = "Hand/Backend/Resources/normalization_bounds.csv"

        self.sampling_rate = 10
        self.window_size = 0.2
        self.interval_size = 0.05

    def start_prediction(self):
        """
        Starts the prediction thread.
        """
        self.running = True
        self.thread = threading.Thread(target=self.predict, daemon=True)
        self.thread.start()

    def stop_prediction(self):
        """
        Stops the prediction thread.
        """
        self.running = False
        if self.thread:
            self.thread.join()

    def predict(self):
        """
        Predicts the gesture using the trained model.
        """
        try:
            model = tf.keras.models.load_model(self.model_file_path)
            min_vals, max_vals = self.read_normalization_bounds()
            start_time = time.time()

            while self.running:
                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time >= self.interval_size:
                    window = self.signal_receiver.get_last_n_signals(int(self.window_size * self.sampling_rate))
                    features = self.feature_extractor.extract_features(window)
                    normalized_features = (features - min_vals) / (max_vals - min_vals + 1e-8)
                    normalized_features = normalized_features.reshape(1, -1)
                    predictions = model.predict(normalized_features, verbose=0)

                    with self.buffer_lock:
                        self.last_prediction = predictions

                    class_prediction = np.argmax(predictions)
                    gesture_map = {0: "open", 1: "fist", 2: "peace", 3: "point", 4: "thumb"}
                    gesture = gesture_map.get(class_prediction, "unknown")
                    print(f"Predicted gesture: {gesture}")

                    start_time = current_time

        except Exception as e:
            with self.buffer_lock:
                self.last_error = e
            self.running = False
    
    def read_normalization_bounds(self):
        '''
        Read the min and max values of the features for normalization.

        :param input_bounds_file_name: The name of the input bounds file.
        '''
        with open(self.normalization_bounds_file_name, mode='r', newline='') as file:
            reader = csv.reader(file)
            min_vals = next(reader)
            max_vals = next(reader)

        return np.array(min_vals, dtype=float), np.array(max_vals, dtype=float)

    def get_prediction(self):
        """
        Retrieves the last prediction made by the model.

        :return: The index of the gesture with the highest predicted probability.
        """
        with self.buffer_lock:
            if self.last_prediction is not None:
                predicted_index = np.argmax(self.last_prediction)
                return predicted_index
            else:
                return None

    def get_error(self):
        with self.buffer_lock:
            return self.last_error
