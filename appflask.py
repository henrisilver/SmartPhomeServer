from flask import Flask
import RPi.GPIO as GPIO

app = Flask(__name__)
status = False

@app.route("/on/")
def on():
    GPIO.output(17, True)
    global status
    status = True
    return "LED on"

@app.route("/off/")
def off():
    GPIO.output(17, False)
    global status
    status = False
    return "LED off"

@app.route("/status/")
def status():
    str = "Led is"
    global status
    if status:
        str = str + " on"
    else:
        str = str + " off"
    return str

if __name__ == "__main__":
    try:
        status = False
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17, GPIO.OUT)
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        # print("\n\nDEU\n\n")
        GPIO.cleanup()
