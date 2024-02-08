import serial
import time

# Function to initialize the serial connection
def init_serial_connection():
    try:
        ser = serial.Serial(
            port='COM7',     # Set to your COM port number
            baudrate=576000,   # Set to your baud rate
            timeout=1        # Set read timeout, adjust as necessary
        )

        # Check if the serial port is open; if not, open it
        if not ser.is_open:
            ser.open()
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port: {e}")
        return None

# Function to send a command to the robot
def send_command(ser, command):
    encoded_command = command.encode()  # Encode the command to bytes
    ser.write(encoded_command)
    time.sleep(0.05)  # Give the device some time to respond

# Function to read the response from the robot
def read_response(ser):
    try:
        # Attempt to read and decode the response, ignoring decoding errors
        response = ser.readline().decode('utf-8', 'ignore').strip()
    except Exception as e:
        print(f"Error reading response: {e}")
        response = ''  # Return an empty string in case of an error
    return response

# Function to read commands from a file and send them one by one, waiting for user confirmation
def read_commands_from_file_and_send(ser):
    filename = input("Enter filename: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                # Show the command to the user and wait for Enter press
                print(f"Next command to send: {line.strip()}")
                user_decision = input("Press Enter to send this command, or type 'q' to stop: ")  # Correctly capture user input here

                # Check if user wants to quit after seeing the command
                if user_decision.lower() == 'q':  # Correctly check the lowercased input
                    print("Stopping command execution from file.")
                    break

                # Send the command after confirmation
                send_command(ser, line.strip() + "\r\n")
                response = read_response(ser)
                print("Response:", response)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading from file: {e}")

# Send commands from a file and do not wait for user confirmation.
dt = 0.2 # step in seconds
def read_commands_from_file_and_send_periodically(ser):
    filename = input("Enter filename: ")
    try:
        with open(filename, "r") as file:
            for line in file:
                # Show the command to the user and wait for Enter press
                print(f"Next command to send: {line.strip()}")
                #user_decision = input("Press Enter to send this command, or type 'q' to stop: ")  # Correctly capture user input here

                # Check if user wants to quit after seeing the command
                #if user_decision.lower() == 'q':  # Correctly check the lowercased input
                #    print("Stopping command execution from file.")
                #    break

                # edit dt value in command to be sent. dt is in milliseconds but variable dt is in seconds
                if line.strip().startswith("dt:"):
                    dt_str = "dt: " + str(int(dt*1000))
                    line = line.strip().replace("dt: ", dt_str)

                send_command(ser, line.strip() + "\r\n")
                response = read_response(ser)
                print("Response:", response)
                time.sleep(dt)
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading from file: {e}")

# Main function to run the terminal interface
def run_terminal_interface():
    ser = init_serial_connection()
    if ser is None:
        print("Failed to initialize serial connection. Exiting.")
        return

    print("Robot Motor Controller Interface")
    print("Type 'get' to fetch the current configuration or 'set <command>' to send a command. Type 'exit' to quit.")
    
    while True:
        user_input = input("Enter command: ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break
        elif user_input.lower() == "get":
            send_command(ser, "\r\n")  # Sending empty command to fetch current configuration
            response = read_response(ser)
            print("Received back:", response)
        elif user_input.lower().startswith("set "):
            # Extract the command part after "set "
            command = user_input[4:]
            send_command(ser, command + "\r\n")  # Add carriage return and newline as per your device protocol
            response = read_response(ser)
            #angle: j1: -0.032971, j2: 0.858527, j3: -2.641633, j4: 0.010468, j5: 0.213064, j6: -0.373927, safemode: 0, brake: 0, gripper: 0, dt: 1000
            #angle: j1: -0.032971, j2: 0.0, j3: 0.0, j4: 0.0, j5: 0.0, j6: 0.0, safemode: 0, brake: 0, gripper: 0, dt: 1000
            print("Command sent. Response:", response)
        elif user_input.lower() == "f":
            read_commands_from_file_and_send(ser)
        elif user_input.lower() == "fp":
            read_commands_from_file_and_send_periodically(ser)
        else:
            print("Invalid command. Please use 'get' or 'set <command>'.")

    # Close the serial port
    ser.close()

if __name__ == "__main__":
    run_terminal_interface()
