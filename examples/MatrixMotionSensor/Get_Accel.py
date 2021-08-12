import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SetI2C(1, "MotionSensor")

while True:
    print("===============================================================")
    print("ax=", Mini1.I2C1.getAccel("X"))
    print("ay=", Mini1.I2C1.getAccel("Y"))
    print("az=", Mini1.I2C1.getAccel("Z"))
    time.sleep(0.5)

