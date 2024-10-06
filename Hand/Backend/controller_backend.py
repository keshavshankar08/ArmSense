from signal_receiver import *
from data_collector import *
from trainer import *
from predictor import *
from feature_extractor import *
import time
import numpy as np

class ControllerBackend:
    def __init__(self, sampling_rate=100, window_size=.2, interval_size=.05):
        '''
        Initialize the ControllerBackend with the given sampling rate, window size, and interval size.

        :param sampling_rate: Sampling rate in Hz
        :param window_size: Window size in seconds
        :param interval_size: Interval size in seconds
        '''
        self.sampling_rate = sampling_rate
        self.window_size = window_size
        self.interval_size = interval_size

        self.signal_receiver = SignalReceiver(self.sampling_rate)
        self.data_collector = DataCollector(self.signal_receiver, self.sampling_rate, self.window_size, self.interval_size)

if __name__ == '__main__':
    controller_backend = ControllerBackend()
    controller_backend.signal_receiver.connect()
    controller_backend.signal_receiver.start_reception()
    time.sleep(1)

    controller_backend.data_collector.start_collection(1) # say 1 is fist
    time.sleep(3)
    controller_backend.data_collector.stop_collection()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        controller_backend.data_collector.stop_collection()
        controller_backend.signal_receiver.stop_reception()