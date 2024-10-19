import sys
sys.path.append('.')

import time

from Hand.Backend.controller_backend import *

if __name__ == '__main__':
    # ----- Setup -----
    # Create backend instance
    backend = be.ControllerBackend()

    # Connect to the serial port
    backend.signal_receiver.connect()

    # Start receiving signals
    backend.signal_receiver.start_reception()

    # Wait for a second
    time.sleep(1)


    # ----- Data Collection -----
    # Start a data collection phase for "open" gesture, lasting 3 seconds
    backend.data_collector.start_collection(0)
    time.sleep(3)
    backend.data_collector.stop_collection()

    # Start a data collection phase for "fist" gesture, lasting 3 seconds
    backend.data_collector.start_collection(1)
    time.sleep(3)
    backend.data_collector.stop_collection()

    # Start a data collection phase for "peace" gesture, lasting 3 seconds
    backend.data_collector.start_collection(2)
    time.sleep(3)
    backend.data_collector.stop_collection()

    # Start a data collection phase for "thumbs up" gesture, lasting 3 seconds
    backend.data_collector.start_collection(3)
    time.sleep(3)
    backend.data_collector.stop_collection()

    # Start a data collection phase for "point" gesture, lasting 3 seconds
    backend.data_collector.start_collection(4)
    time.sleep(3)
    backend.data_collector.stop_collection()

    # Wait for a second
    time.sleep(1)


    # ----- Data Preperation -----
    # Clean the data
    backend.trainer.clean_data()

    # Normalize the data
    backend.trainer.normalize_data()


    # ----- Model training -----
    # Train the model
    backend.trainer.train_model()

    # Wait for a second
    time.sleep(1)


    # ----- Gesture Predicting -----


