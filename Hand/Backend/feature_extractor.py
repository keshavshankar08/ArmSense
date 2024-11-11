import numpy as np
import scipy as sp

class FeatureExtractor:
    def __init__(self):
        """
        Initializes the FeatureExtractor.
        """

    def extract_features(self, window_signals):
        """
        Extracts features for a window.

        :param window_signals: The signals in the window.
        """
        features = []
        for i in range(8):
            features.append(round(self.integrated_emg(window_signals[:, i]), 2))
            features.append(round(self.mean_square_value(window_signals[:, i]), 2))
            features.append(round(self.variance(window_signals[:, i]), 2))
            features.append(round(self.rms(window_signals[:, i]), 2))
            features.append(round(self.kurtosis(window_signals[:, i]), 2))
            features.append(round(self.skewness(window_signals[:, i]), 2))

        return features

    def integrated_emg(self, signal):
        return np.sum(np.abs(signal))

    def mean_square_value(self, signal):
        return np.mean(signal ** 2)

    def variance(self, signal):
        return np.var(signal)

    def rms(self, signal):
        return np.sqrt(np.mean(signal ** 2))

    def kurtosis(self, signal):
        return 0.0
        #return sp.stats.kurtosis(signal)

    def skewness(self, signal):
        return 0.0
        #return sp.stats.skew(signal)
