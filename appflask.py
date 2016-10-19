from flask import Flask
from gpiozero import MotionSensor
import RPi.GPIO as GPIO
import time
import datetime
import threading

app = Flask(__name__)
status = False
presenceTimeStamps = []

def motionSensor():
    sensor = MotionSensor(4)
    global presenceTimeStamps
    global lock
    while True:
    if sensor.motion_detected:
        currentTime = time.time()
        timestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S') 
        presenceTimeStamps.append(timestamp)
        time.sleep(2)

@app.route("presence")
def presence():
    global presenceTimeStamps
    stamps = ""
    for ts in presenceTimeStamps:
        stamps = stamps + str(ts)
    return stamps

@app.route("light/on/")
def on():
    GPIO.output(17, True)
    global status
    status = True
    return "LED on"

@app.route("light/off/")
def off():
    GPIO.output(17, False)
    global status
    status = False
    return "LED off"

@app.route("light/status/")
def status():
    global status
    if status:
        str = "on"
    else:
        str = "off"
    return str

if __name__ == "__main__":
    try:
        status = False
        t = threading.Thread(target=motionSensor)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        app.run(host="189.5.253.103", port=5000, debug=True)
    finally:
        GPIO.cleanup()
