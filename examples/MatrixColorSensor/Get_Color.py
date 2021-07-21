import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)

while True:
    print("===============================================================")
    print("R=", Mini1.I2C1.getColor("R"))
    print("G=", Mini1.I2C1.getColor("G"))
    print("B=", Mini1.I2C1.getColor("B"))

    print("C=", Mini1.I2C1.getColor("C"))
    print("M=", Mini1.I2C1.getColor("M"))
    print("Y=", Mini1.I2C1.getColor("Y"))
    print("K=", Mini1.I2C1.getColor("K"))

    time.sleep(0.5)

