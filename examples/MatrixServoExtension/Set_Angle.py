import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SetI2C(1, "ServoExtension")

while True:
    print("===============================================================")

    channel = 1
    angle = 0
    Mini1.SE1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 2
    angle = 60
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 3
    angle = 120
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 4
    angle = 180
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 5
    angle = 0
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 6
    angle = 60
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 7
    angle = 120
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

    channel = 8
    angle = 180
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(0.25)

