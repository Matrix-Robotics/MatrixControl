import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini")

t = 1
limit = 100
step = 5

try:
    while True:
        # get Button click, 1 means true, 0 means false
        print("BTN1:", Mini1.BTN1.get())
        print("BTN2:", Mini1.BTN2.get())
        # get Analog data
        print("A1 ANG:", Mini1.A1.getANG())
        print("A2 ANG:", Mini1.A2.getANG())
        print("A3 ANG:", Mini1.A3.getANG())
        # get Digital data
        print("D1 DIG:", Mini1.D1.getDIG())
        print("D2 DIG:", Mini1.D2.getDIG())
        print("D3 DIG:", Mini1.D3.getDIG())

        # set Motor speed
        Mini1.M1.set(50)
        Mini1.M2.set(50)
        # set RGB LED
        Mini1.RGB1.setRGB(0, 0, 255)
        Mini1.RGB2.setRGB(0, 0, 0)
        time.sleep(t)

        Mini1.M1.set(-50)
        Mini1.M2.set(-50)
        Mini1.RGB1.setRGB(0, 0, 0)
        Mini1.RGB2.setRGB(0, 0, 255)
        time.sleep(t)
        print("=========================")

except KeyboardInterrupt:
    Mini1.close()
    print("DeviceClose")
