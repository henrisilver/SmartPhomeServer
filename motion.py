from gpiozero import MotionSensor
import time

i = 0
pir = MotionSensor(4)
while True:
    if pir.motion_detected:
        print("Motion detected! ", i)
        i = i + 1
        time.sleep(2)
