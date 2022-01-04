import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SetI2C(1, "LaserSensor")

while True:
    print("===============================================================")
    print("range=", Mini1.I2C1.getDistance())
    time.sleep(0.5)
