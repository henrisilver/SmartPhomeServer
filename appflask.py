from flask import Flask, jsonify
from gpiozero import MotionSensor
import datetime
import os
import pygame
import RPi.GPIO as GPIO
import threading
import time

app = Flask(__name__)
status = False
status2 = False
presenceTimeStamps = {}

def motionSensor():
    sensor = MotionSensor(4)
    global presenceTimeStamps
    index = 0
    while True:
        if sensor.motion_detected:
            currentTime = time.time()
            timestamp = datetime.datetime.fromtimestamp(currentTime).strftime('%Y-%m-%d %H:%M:%S') 
            ts = {}
            timestamp = timestamp.split()
            ts["date"] = timestamp[0]
            ts["time"] = timestamp[1]
            presenceTimeStamps[str(index)] = ts
            index = index + 1
            time.sleep(2)

@app.route("/music/play=<song>")
def playSong(song):
    try:
        songName = "./songs/" + str(song) + ".mp3"
        pygame.mixer.music.load(songName)
        pygame.mixer.music.play()
        return "Playing " + str(song)
    except Exception as e:
        print (e)
        return "Error"

@app.route("/music/stop")
def stopPlayback():
    pygame.mixer.music.stop()
    return "Playback stopped"

@app.route("/music/getsonglist")
def songList():
    songList = {}
    index = 1
    for file in os.listdir("./songs"):
        if file.endswith(".mp3"):
            songList[str(index)] = file[:-4]
            index = index + 1
    return jsonify(**songList)

@app.route("/presence/getlist")
def presenceGetList():
    global presenceTimeStamps
    
    return jsonify(**presenceTimeStamps)

@app.route("/presence/clear")
def presenceClearList():
    global presenceTimeStamps
    presenceTimeStamps = []
    return "Timestamp list cleared."

@app.route("/light2/on/")
def on2():
    GPIO.output(27, True)
    global status2
    status2 = True
    return "LED on"

@app.route("/light2/off/")
def off2():
    GPIO.output(27, False)
    global status2
    status2 = False
    return "LED off"

@app.route("/light2/status/")
def status2():
    global status2
    if status2:
        str = "on"
    else:
        str = "off"
    return str

@app.route("/light/on/")
def on():
    GPIO.output(17, True)
    global status
    status = True
    return "LED on"

@app.route("/light/off/")
def off():
    GPIO.output(17, False)
    global status
    status = False
    return "LED off"

@app.route("/light/status/")
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
        t.start()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        pygame.mixer.init()
        app.run(host="189.5.253.103", port=5000, debug=True)
    finally:
        GPIO.cleanup()
