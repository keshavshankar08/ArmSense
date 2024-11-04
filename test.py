import sys
sys.path.append('.')

import time
import Hand.Backend.controller_backend as be

if __name__ == '__main__':
    # ----- Setup -----
    # Create backend instance
    backend = be.ControllerBackend()

    # Connect to the serial port
    # backend.signal_receiver.connect('/dev/tty.usbserial-0001', 115200)
    backend.signal_receiver.connect()
    time.sleep(5)

    # Start receiving signals
    # backend.signal_receiver.start_reception(100)

    # Wait for a second
    time.sleep(1)
    

    """ # ----- Data Collection -----
    # Start a data collection phase for "open" gesture, lasting 3 seconds
    backend.data_collector.start_collection(0, 100, 0.2, 0.05)
    time.sleep(3)
    backend.data_collector.stop_collection("Hand/Backend/Resources/data.csv")

    # Start a data collection phase for "fist" gesture, lasting 3 seconds
    backend.data_collector.start_collection(1, 100, 0.2, 0.05)
    time.sleep(3)
    backend.data_collector.stop_collection("Hand/Backend/Resources/data.csv")

    # Wait for a second
    time.sleep(1)


    # ----- Data Preperation -----
    # Clean the data
    backend.trainer.clean_data("Hand/Backend/Resources/data.csv", "Hand/Backend/Resources/cleaned_data.csv")

    # Normalize the data
    backend.trainer.normalize_data("Hand/Backend/Resources/cleaned_data.csv", "Hand/Backend/Resources/normalized_data.csv", "Hand/Backend/Resources/normalize_bounds.csv")

    # Wait for a second
    time.sleep(1)


    # ----- Model training -----
    # Train the model
    backend.trainer.train_model("Hand/Backend/Resources/normalized_data.csv", "Hand/Backend/Resources/model.h5")

    # Wait for a second
    time.sleep(1) """


    # ----- Gesture Predicting -----
    # Read in normalization bounds
    min_vals, max_vals = backend.trainer.read_normalization_bounds("Hand/Backend/Resources/normalize_bounds.csv")

    # Start predicting
    backend.predictor.start_prediction("Hand/Backend/Resources/model.h5", min_vals, max_vals, 100, 0.2, 0.05)
    time.sleep(5)
    backend.predictor.stop_prediction()


