import sys
sys.path.append('.')

from Backend.signal_receiver import *
from Backend.data_collector import *
from Backend.trainer import *
from Backend.predictor import *
from Backend.feature_extractor import *

class ControllerBackend:
    def __init__(self):
        '''
        Initialize the ControllerBackend with the given sampling rate, window size, and interval size.
        '''
        self.signal_receiver = SignalReceiver()
        self.data_collector = DataCollector(self.signal_receiver)
        self.trainer = Trainer()
        self.predictor = Predictor(self.signal_receiver)