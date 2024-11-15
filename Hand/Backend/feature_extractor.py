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
        if window_signals is None or len(window_signals) == 0:
            return

        features = []
        for i in range(8):
            features.append(round(self.rms(window_signals[:, i]), 2))
            features.append(round(self.variance(window_signals[:, i]), 2))
            features.append(round(self.mean_absolute_value(window_signals[:, i]), 2))
            features.append(round(self.slope_sign_change(window_signals[:, i]), 2))
            features.append(round(self.zero_crossing(window_signals[:, i]), 2))
            features.append(round(self.waveform_length(window_signals[:, i]), 2))

        return features

    def rms(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        return (sum(x ** 2 for x in signal) / len(signal)) ** 0.5

    def variance(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        mean = sum(signal) / len(signal)
        return sum((x - mean) ** 2 for x in signal) / len(signal)

    def mean_absolute_value(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        return sum(abs(x) for x in signal) / len(signal)

    def slope_sign_change(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        return sum(1 for i in range(1, len(signal) - 1) if (signal[i] - signal[i - 1]) * (signal[i] - signal[i + 1]) > 0)

    def zero_crossing(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        return sum(1 for i in range(1, len(signal)) if signal[i - 1] * signal[i] < 0)

    def waveform_length(self, signal):
        if all(x == 0 for x in signal):
            return 0.0
        return sum(abs(signal[i] - signal[i - 1]) for i in range(1, len(signal)))
