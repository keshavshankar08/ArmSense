import Hand.Backend.signal_receiver as sr
import Hand.Backend.data_collector as dc
import Hand.Backend.trainer as tr
import Hand.Backend.predictor as pr

class ControllerBackend:
    def __init__(self):
        '''
        Initializes the ControllerBackend.
        '''
        self.signal_receiver = sr.SignalReceiver()
        self.data_collector = dc.DataCollector(self.signal_receiver)
        self.trainer = tr.Trainer()
        self.predictor = pr.Predictor(self.signal_receiver)