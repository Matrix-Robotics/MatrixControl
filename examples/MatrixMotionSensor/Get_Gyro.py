import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SetI2C(1, "MotionSensor")

while True:
    print("===============================================================")
    print("gx=", Mini1.I2C1.getGyro("X"))
    print("gy=", Mini1.I2C1.getGyro("Y"))
    print("gz=", Mini1.I2C1.getGyro("Z"))
    time.sleep(0.5)

