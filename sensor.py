import serial
import matplotlib.pyplot as plt
import re

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)  # Change the port accordingly

# Initialize lists to store data
timestamps = []
sensor_data = []
# Read and parse serial data
plt.interactive(True)
def update_plot(timestamps,sensor_data):
    # Plot the data
    plt.plot(timestamps, sensor_data)
    plt.xlabel('Time')
    plt.ylabel('Sensor Data')
    plt.title('Sensor Data over Time')
    plt.grid(True)
    plt.clf()  # Clear the plot for the next iteration

while True:
    ser.readline().decode('utf-8').rstrip()
    line = "Teststring"
    if line:
        print("Received line:", line)  # Debugging output

        # Split the received string by comma
        data = line.split(',')
        if len(data) == 2:
            timestamp_str = data[0].strip()
            sensor_data_str = data[1].strip()

            # Remove non-numeric characters from sensor data string
            sensor_data_str = re.sub(r'\D+', '', sensor_data_str)

            # Check if both timestamp and sensor data are valid strings
            if timestamp_str and sensor_data_str:
                timestamp = float(timestamp_str)
                sensor = float(sensor_data_str)
                timestamps.append(timestamp)
                sensor_data.append(sensor)
                print("Timestamp:", timestamp, "Data:", sensor)
            else:
                print("Skipping line due to empty timestamp or sensor data:", line)
        else:
            print("Skipping line due to incorrect format:", line)

        update_plot(timestamps,sensor_data)

# Close serial connection (This will never execute in an infinite loop)
ser.close()
