import Hand.Backend.controller_backend as cb
import time
import asyncio

controller_backend = cb.ControllerBackend()

asyncio.run(controller_backend.signal_receiver.find_devices())
asyncio.run(controller_backend.signal_receiver.set_device("MDT UART Service"))

controller_backend.signal_receiver.start_reception()

time.sleep(5)
controller_backend.data_collector.clear_data()
controller_backend.data_collector.start_collection(0)
time.sleep(5)
controller_backend.data_collector.stop_collection()

controller_backend.signal_receiver.stop_reception()

