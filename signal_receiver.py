import serial

class signal_receiver:
    def __init__(self):
        self.device = serial.Serial("/dev/tty.usbserial-0001", 115200)
        self.signal = ""
    
    def receive_signal(self):
        while True:
            try:
                self.signal = self.device.readline()[0:-5]
            except KeyboardInterrupt:
                break
        return
    
if __name__ == "__main__":
    receiver = signal_receiver()
    receiver.receive_signal()