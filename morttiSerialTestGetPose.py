import serial
import time

# Configure the serial connection
ser = serial.Serial(
    port='COM7',     # Set to your COM port number
    baudrate=576000,   # Set to your baud rate
    timeout=1        # Set read timeout, adjust as necessary
)

# Check if the serial port is open; if not, open it
if not ser.is_open:
    ser.open()


buffer_command = "\r\n"
while True:
    
    #ser.write(buffer_command.encode())
    ser.write(b"\r\n")
    # Give the device some time to respond
    time.sleep(0.5)

    # Read the response
    response =  response = ser.readline().decode().strip() #ser.read_all()

    # Print the response
    print("Received back:", response)
    # example response:
    # Received back: angle: j1: -0.032288, j2: 0.857046, j3: -2.639949, j4: 0.010468, j5: 0.212749, j6: -0.373927, safemode: 1, brake: 1, gripper: 0, dt: 1844636230
    
    time.sleep(5)

# Close the serial port
ser.close()
