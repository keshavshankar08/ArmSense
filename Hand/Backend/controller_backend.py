import sys
sys.path.append('.')

from Hand.Backend.signal_receiver import *
from Hand.Backend.data_collector import *
from Hand.Backend.trainer import *
from Hand.Backend.predictor import *
from Hand.Backend.feature_extractor import *

class ControllerBackend:
    def __init__(self):
        '''
        Initializes the ControllerBackend.
        '''
        self.signal_receiver = SignalReceiver()
        self.data_collector = DataCollector(self.signal_receiver)
        self.trainer = Trainer()
        self.predictor = Predictor(self.signal_receiver)