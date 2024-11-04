import asyncio
from bleak import BleakScanner

async def find_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found device: {device.name}, Address: {device.address}")

asyncio.run(find_devices())