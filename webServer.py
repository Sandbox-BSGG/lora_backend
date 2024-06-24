import serial
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import re

SERIAL_PORT = 'COM3'
BAUD_RATE = 9600
ser = serial.Serial(SERIAL_PORT, BAUD_RATE,timeout=1)  # Change the port accordingly
app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8080",
]


@app.get("/")
async def main():
    return {"message": "Hello World"}


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

timestamps = []
sensor_data = []

@app.get("/data")
def readData():
    getSensorData()
    data = {"timestamps": timestamps, "sensor": sensor_data}
    return data


def getSensorData():

    try:
        line = ser.readline().decode('utf-8').rstrip()
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

    except:
        None
