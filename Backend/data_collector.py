from collections import deque

class DataCollector:
    def __init__(self, signal_receiver, feature_extractor):
        self.signal_receiver = signal_receiver
        self.feature_extractor = feature_extractor
        self.signal_buffer = deque(maxlen=self.buffer_size)

    def start_collection(self, gesture_class):
        # Start polling every 50ms
            # get latest window and use feature extractor to get features
            # save feature to buffer
        pass
    
    def stop_collection(self):
        # call save_data
        pass

    def save_data(self, filename):
        # write the buffer to a file
        pass