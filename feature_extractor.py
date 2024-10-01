import numpy as np
import serial

class feature_extractor:
    def __init__(self, port, baud_rate):
        self.device = serial.Serial(port, baud_rate, timeout=1)
        self.signal = np.array([])
        self.features = np.array([])
    
    def receive_signal(self, rate):
        # read signal from serial at rate
        # store signal in self.signal
        pass

    def read_signal(self, rate):
        # 1st run
        # read signal from self.signal at rate
        # once 200ms window signals collected
        # pass to compute feature matrix method

        # concecutive runs
        # once another 50ms signals collected
        # use 50-200ms of buffer + 50ms new signals as new 200ms window
        # pass to compute feature matrix method
        # repeat
        pass

    def compute_feature_matrix(self, signals):
        # compute feature matrix from signal
        # store in self.features
        pass

if __name__ == "__main__":
    pass