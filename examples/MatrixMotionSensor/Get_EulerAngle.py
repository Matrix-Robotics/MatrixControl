import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)
Mini1.SetI2C(1, "MotionSensor")

while True:
    print("===============================================================")
    print("Roll=", Mini1.I2C1.getRoll())
    print("Pitch=", Mini1.I2C1.getPitch())
    print("Yaw=", Mini1.I2C1.getYaw())
    time.sleep(0.5)

