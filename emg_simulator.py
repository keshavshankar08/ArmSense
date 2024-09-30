import numpy as np
import time
import serial

class emg_simulator:
    def __init__(self):
        pass
    
    def generate_signal(self, contraction_time, relaxation_time):
        signal = np.zeros(2000)
        signal[0:contraction_time*500] = 100
        signal[contraction_time*500:(contraction_time+relaxation_time)*500] = 0
        return signal

    def write_signal(self, signal):
        start_time = time.time()
        for value in signal:
            #print(value)
            time.sleep(0.001)
        print(f"Time taken: {time.time() - start_time}")


if __name__ == "__main__":
    emg_sim = emg_simulator()
    signal = emg_sim.generate_signal(2, 2)
    emg_sim.write_signal(signal)