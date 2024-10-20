import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")

# Ensure that you're using the correct port
ser = serial.Serial('/dev/cu.usbserial-0001', 115200)  # Update this if needed
