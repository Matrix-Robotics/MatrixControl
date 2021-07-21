import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)

while True:
    print("===============================================================")
    print("grayscale=", Mini1.I2C1.getGrayscale())
    time.sleep(0.5)
