from signal_receiver import *
from data_collector import *
from trainer import *
from predictor import *
from feature_extractor import *
import time
import numpy as np

class ControllerBackend:
    def __init__(self):
        self.signal_receiver = SignalReceiver(port='/dev/tty.usbserial-0001', baud_rate=115200, sampling_rate=100, buffer_size=1000)
        self.feature_extractor = FeatureExtractor(sampling_rate=100, window_duration=.2)

if __name__ == '__main__':
    controllerBackend = ControllerBackend()
    controllerBackend.signal_receiver.start()

    time.sleep(1)

    window = np.array(controllerBackend.signal_receiver.get_last_n_signals(20))
    features = controllerBackend.feature_extractor.extract_features(window)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controllerBackend.signal_receiver.stop()