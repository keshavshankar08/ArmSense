import serial
import serial.tools.list_ports

# List available ports to confirm the correct one
ports = serial.tools.list_ports.comports()
print("Available serial ports:")
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")

# Open the serial connection
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)  # Ensure port is correct

try:
    print("Reading data from serial port...")
    while True:
        # Read and decode the line from serial
        line = ser.readline().decode('utf-8', errors='ignore').strip()
        if line:
            print(f"Received: {line}")
except KeyboardInterrupt:
    print("Stopped by user.")
finally:
    ser.close()
    print("Serial port closed.")