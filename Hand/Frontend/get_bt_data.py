import asyncio
import os
import sys

# Ensure the Backend directory is in the path
sys.path.append(os.path.abspath('../Backend'))
from Backend.signal_receiver import SignalReceiver

async def main():
    # Initialize the SignalReceiver
    signal_receiver = SignalReceiver()

    # Connect to the Bluetooth device
    try:
        await signal_receiver.connect()
        print("Connected to Bluetooth device.")
    except Exception as e:
        print(f"Failed to connect to Bluetooth device: {e}")
        return

    # Continuously print the received data
    try:
        while True:
            signals = signal_receiver.get_last_n_signals(1)  # Get the most recent signal
            if signals is not None:
                print("Received signal:", signals)
            await asyncio.sleep(1)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Stopping data reception.")
    finally:
        signal_receiver.disconnect()

if __name__ == "__main__":
    asyncio.run(main())