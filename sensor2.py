import serial
import matplotlib.pyplot as plt
import re
import csv
from matplotlib.animation import FuncAnimation

SERIAL_PORT = 'COM4'
BAUD_RATE = 9600
# Open serial connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)  # Change the port accordingly
# ser.flush()

# Initialize lists to store data
timestamps = []
sensor_data = []


# Read and parse serial data
def read_and_process_data():
    line = ser.readline().decode('utf-8').rstrip()
    data = line.split(",")
    timestamp_str = data[0].strip()
    sensor_data_str = data[1].strip()

    sensor_data_str = re.sub(r'\D+', '', sensor_data_str)

    """timestamp = float(timestamp_str)
    sensor = float(sensor_data_str)
    timestamps.append(timestamp)
    sensor_data.append(sensor)"""


def update_plot(frame):
    # Plot the data
    plt.plot(timestamps, sensor_data)
    plt.xlabel('Time')
    plt.ylabel('Sensor Data')
    plt.title('Sensor Data over Time')
    plt.grid(True)
    plt.clf()  # Clear the plot for the next iteration


def on_close(event):
    with open('arduino_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time', 'Sensordata'])
        for x, s1, s2 in zip(timestamps, sensor_data):
            writer.writerow([x, s1])


# Register the callback function for when the plot window is closed
fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', on_close)

ani = FuncAnimation(fig, update_plot, interval=1)
plt.show()

# Close serial connection (This will never execute in an infinite loop)
ser.close()
