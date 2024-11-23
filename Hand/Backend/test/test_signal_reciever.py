import sys
import os
import time
import asyncio
import logging
import threading

# Configure logging to output to the console
logging.basicConfig(
    level=logging.DEBUG,                    # Set the level of logging you want
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Get the parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

test="test"

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from signal_receiver import SignalReceiver

async def start():
    signal = SignalReceiver()
    await signal.connect(1,1)
    time.sleep(5)
    reception_thread = threading.Thread(target=signal.start_reception, args={100})
    reception_thread.start()
    # signal.start_reception(100)
    time.sleep(5)

signal = SignalReceiver()
# asyncio.run(signal.connect(1,1))
# asyncio.run(start())

# reception_thread = threading.Thread(target=signal.start_reception, args={100})
# reception_thread.start()
# loop = asyncio.get_event_loop()
# loop.run_until_complete(signal.start_reception())

# asyncio.run(signal.start_reception())

# run = asyncio.create_task(signal.start_reception())
# signal.start_reception()
signal.start_reception(100)
# signal.connect()
while not signal.client.is_connected:
    time.sleep(0.001)
    print("Waiting for subscription")
    # print(signal.running)
print("Started Reception")
signal.counter = 0
time.sleep(20)
print(signal.counter)
print("Stopping Reception")
signal.stop_reception()
print("Stopped Reception")

# time.sleep(20)

# signal.stop_reception()

print("Done")