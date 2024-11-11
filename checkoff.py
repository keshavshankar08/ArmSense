import sys
import time
sys.path.append('.')

import Hand.Backend.controller_backend as be


def data_collection():
    # ----- Data Collection -----
    # Measure time to collect data for "open" gesture
    start_time = time.time()
    backend.data_collector.start_collection(0, 100, 0.2, 0.05)
    time.sleep(3)
    backend.data_collector.stop_collection("Hand/Backend/Resources/data.csv")
    end_time = time.time()
    open_gesture_latency = end_time - start_time
    print(f"Time to collect data for 'open' gesture: {open_gesture_latency:.4f} seconds")

    # Measure time to collect data for "fist" gesture
    start_time = time.time()
    backend.data_collector.start_collection(1, 100, 0.2, 0.05)
    time.sleep(3)
    backend.data_collector.stop_collection("Hand/Backend/Resources/data.csv")
    end_time = time.time()
    fist_gesture_latency = end_time - start_time
    print(f"Time to collect data for 'fist' gesture: {fist_gesture_latency:.4f} seconds")

    # Wait for a second
    time.sleep(1)
    # -----------------------------------------------------------------------------


def data_preparation():
    # ----- Data Preperation -----
    # Clean the data
    start_time = time.time()
    backend.trainer.clean_data("Hand/Backend/Resources/data.csv", "Hand/Backend/Resources/cleaned_data.csv")
    end_time = time.time()
    clean_latency = end_time - start_time
    print(f"Time to clean data: {clean_latency:.4f} seconds")

    # Normalize the data
    start_time = time.time()
    backend.trainer.normalize_data("Hand/Backend/Resources/cleaned_data.csv", "Hand/Backend/Resources/normalized_data.csv", "Hand/Backend/Resources/normalize_bounds.csv")
    end_time = time.time()
    normalize_latency = end_time - start_time
    print(f"Time to normalize data: {normalize_latency:.4f} seconds")

    # Wait for a second
    time.sleep(1)
    # -----------------------------------------------------------------------------


def model_training():
    # ----- Model training -----
    # Train the model
    start_time = time.time()
    backend.trainer.train_model("Hand/Backend/Resources/data.csv", "Hand/Backend/Resources/model.h5")
    end_time = time.time()
    train_latency = end_time - start_time
    print(f"Time to train: {train_latency:.4f} seconds")

    # Wait for a second
    time.sleep(1)
    # -----------------------------------------------------------------------------
    

def gesture_predicting():
    # ----- Gesture Predicting -----
    # Read in normalization bounds
    start_time = time.time()
    min_vals, max_vals = backend.trainer.read_normalization_bounds("Hand/Backend/Resources/normalize_bounds.csv")
    end_time = time.time()
    read_latency = end_time - start_time
    print(f"Time to read bound data: {read_latency:.4f} seconds")

    # Wait for a second
    time.sleep(5)

    # Start predicting
    backend.predictor.start_prediction("Hand/Backend/Resources/model.h5", min_vals, max_vals, 100, 0.2, 0.05)
    time.sleep(60)
    backend.predictor.stop_prediction()

    # Wait for a second
    time.sleep(1)


if __name__ == '__main__':
    # ----- Setup -----
    # Create backend instance
    backend = be.ControllerBackend()

    # Measure time to connect to the device
    start_time = time.time()
    backend.signal_receiver.start_reception(100)
    end_time = time.time()
    connect_latency = end_time - start_time
    print(f"Time to connect to the device: {connect_latency:.4f} seconds")

    # Wait for a second
    time.sleep(1)
    # -----------------------------------------------------------------------------
    
    """ open = np.array([1,1,1,1,1,1,1,1])
    fist = np.array([1,2000,1,1,1,1,1,1])
    peace = np.array([1,1,2000,1,1,1,1,1])
    point = np.array([1,1,1,2000,1,1,1,1])
    thumb = np.array([1,1,1,1,2000,1,1,1]) """
    #data_preparation()
    #model_training()
    #gesture_predicting()

    backend.signal_receiver.stop_reception()