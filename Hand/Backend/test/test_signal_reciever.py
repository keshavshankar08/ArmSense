import sys
import os
import time
import asyncio


# Get the parent directory path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

test="test"

# Add the parent directory to sys.path
sys.path.insert(0, parent_dir)

from signal_receiver import SignalReceiver


signal = SignalReceiver(100)

asyncio.run(signal.connect())
# loop = asyncio.get_event_loop()
# loop.run_until_complete(signal.start_reception())
asyncio.run(signal.start_reception())
# run = asyncio.create_task(signal.start_reception())
# signal.start_reception()
print("After Start")

time.sleep(10)

signal.stop_reception()

print("Done")