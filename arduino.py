import serial
import time
import serial.tools.list_ports

# List available ports
ports = serial.tools.list_ports.comports()
portsList = []

for one in ports:
    portsList.append(str(one))
    print(str(one))

# Select COM port
com = input("Select COM Port For Arduino #: ")

use = None
for port in portsList:
    if port.startswith("COM" + str(com)):
        use = "COM" + str(com)
        print(f"Using port: {use}")

if use is None:
    print("Invalid COM port selected.")
    exit()

# Initialize serial connection
serialInst = serial.Serial()
serialInst.baudrate = 9600
serialInst.port = use

try:
    serialInst.open()
    print("Serial port opened successfully.")
except Exception as e:
    print(f"Failed to open serial port: {e}")
    exit()  

def send_command(command):
    serialInst.write(command.encode('utf-8'))
    serialInst.flush()  # Ensure the command is sent immediately
    time.sleep(0.5)  # Small delay to ensure the command is processed
    while serialInst.in_waiting > 0:
        response = serialInst.readline().decode('utf-8').strip()
        print(f"Arduino response: {response}")

# Command loop
while True:
    command = input("Arduino Command (F/S): ").strip()
    if command in ['F', 'S']:
        send_command(command)
    elif command == 'exit':
        print("Exiting...")
        serialInst.close()
        break
    else:
        print("Invalid command. Please enter 'F' to move forward, 'S' to stop, or 'exit' to quit.")
