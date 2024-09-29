import asyncio
from bleak import BleakClient

# Replace with the Bluetooth address of your device
address = "D8:13:2A:7F:2F:FE"

# Characteristic UUID for communication (you need the correct one for your device)
CHARACTERISTIC_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

# Open the file to write data
file_path = "bluetooth_data.txt"

def notification_handler(sender, data):
    message = f"Received message: {data}\n"
    print(message)
    with open(file_path, "a") as file:
        file.write(message)

async def main():
    async with BleakClient(address) as client:
        if client.is_connected:
            print(f"Connected to {address}")

            # Start receiving notifications
            await client.start_notify(CHARACTERISTIC_UUID, notification_handler)

            # Keep the program running to continuously receive data
            await asyncio.sleep(60)  # Adjust the time as needed

            # Stop receiving notifications
            await client.stop_notify(CHARACTERISTIC_UUID)

asyncio.run(main())