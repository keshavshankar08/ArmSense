import numpy as np
import scipy as sp

class FeatureExtractor:
    def __init__(self, sampling_rate, window_duration):
        """
        Initializes the FeatureExtractor.

        :param sampling_rate: Sampling rate in Hz.
        :param window_duration: Duration of the window in seconds.
        """
        self.window_duration = window_duration
        self.window_size = window_duration * sampling_rate

    def extract_features(self, window_signals):
        """
        Extracts features for a window.
        """

        features = []
        for channel in range(window_signals.shape[1]):
            signal = window_signals[:, channel]
            features.extend([np.mean(signal), self.root_mean_square(signal), self.waveform_length(signal), self.skewness(signal), self.kurtosis(signal), self.variance(signal), self.power_spectral_density(signal, fs=self.window_size / self.window_duration), self.spectral_centroid(signal, fs=self.window_size / self.window_duration), self.hjorth_mobility(signal), self.mean_frequency(signal, fs=self.window_size / self.window_duration)])

        feature_vector = np.array(features)

        return feature_vector

    def root_mean_square(self, signal):
        return np.sqrt(np.mean(np.square(signal)))

    def waveform_length(self, signal):
        return np.sum(np.abs(np.diff(signal)))

    def skewness(self, signal):
        return sp.stats.skew(signal)

    def kurtosis(self, signal):
        return sp.stats.kurtosis(signal)

    def variance(self, signal):
        return np.var(signal)

    def power_spectral_density(self, signal, fs):
        f, Pxx = sp.signal.welch(signal, fs=fs)
        return np.mean(Pxx)

    def spectral_centroid(self, signal, fs):
        f, Pxx = sp.signal.welch(signal, fs=fs)
        return np.sum(f * Pxx) / np.sum(Pxx)

    def hjorth_mobility(self, signal):
        diff_signal = np.diff(signal)
        return np.sqrt(np.var(diff_signal) / np.var(signal))

    def mean_frequency(self, signal, fs):
        f, Pxx = sp.signal.welch(signal, fs=fs)
        return np.sum(f * Pxx) / np.sum(Pxx)
