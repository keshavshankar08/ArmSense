import logging
import numpy as np

class FeatureExtractor:
    def __init__(self, signal_receiver, window_duration):
        """
        Initializes the FeatureExtractor.

        :param signal_receiver: Instance of SignalReceiver.
        :param window_duration: Duration of the window in seconds.
        """
        self.signal_receiver = signal_receiver
        self.window_duration = window_duration
        self.window_size = int(self.window_duration * self.signal_receiver.sampling_rate)
        self.running = False

    def extract_features(self):
        """
        Extracts features for most recent window.
        """
        window_signals = self.signal_receiver.get_last_n_signals(self.window_size)
        if window_signals:
            feature_vector = self.compute_feature_matrix(window_signals)
            return feature_vector
        else:
            logging.debug("Insufficient data for feature extraction.")


    def compute_feature_matrix(self, window_signals):
        pass
