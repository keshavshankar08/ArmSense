import serial
import time

# List available ports to confirm the correct one
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
for port in ports:
    print(f"Device: {port.device}, Description: {port.description}")

# Open the serial connection
ser = serial.Serial('/dev/cu.usbserial-0001', 115200, timeout=1)  # Ensure port is correct
output_file = 'semg_data_log.txt'

try:
    with open(output_file, 'w') as f:
        while True:
            # Read the raw bytes and ignore any decoding errors
            line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Received: {line}")  # This will show data in the terminal
            f.write(line + '\n')        # Write to the file
            f.flush()                   # Ensure data is written to file immediately
except KeyboardInterrupt:
    print("Logging stopped by user.")
finally:
    ser.close()
