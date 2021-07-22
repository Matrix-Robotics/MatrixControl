import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SE = I2C(1, "ServoExtension")

channel = 1
angle = 0
Mini1.SE.setAngle(channel, angle)
# print("set channel " + str(channel) + " to " + str(angle))
# time.sleep(0.25)
