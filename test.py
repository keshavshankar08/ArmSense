import Hand.Backend.controller_backend as cb
import time
import asyncio

controller_backend = cb.ControllerBackend()

asyncio.run(controller_backend.signal_receiver.find_devices())
asyncio.run(controller_backend.signal_receiver.set_device("MDT UART Service"))

controller_backend.signal_receiver.start_reception()
time.sleep(10)
controller_backend.signal_receiver.stop_reception()

