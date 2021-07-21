import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)

while True:
    print("===============================================================")

    channel = 1
    angle = 180
    Mini1.I2C1.setAngle(channel, angle)
    print("set channel " + str(channel) + " to " + str(angle))
    time.sleep(1)

    Mini1.I2C1.ChannelRelease(channel)
    print("set channel " + str(channel) + " release")
    time.sleep(0.25)
