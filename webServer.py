import serial
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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


@app.get("/data")
def readData():
    data = {"timestamps": [13.30,13.40,13.50,13.60,14,14.10], "sensor": [20, 25, 21, 15, 10,30]}
    return data


def getSensorData():
    SERIAL_PORT = 'COM4'
    BAUD_RATE = 9600
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE)  # Change the port accordingly
    timestamps = []
    sensor_data = []

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

    # Close serial connection (This will never execute in an infinite loop)
    ser.close()
    return timestamps, sensor_data
