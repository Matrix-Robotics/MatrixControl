import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)

color_dict = {
    0: "Black",
    1: "White",
    2: "Cyan",
    3: "Ocean",
    4: "Blue",
    5: "Violet",
    6: "Magenta",
    7: "Raspberry",
    8: "Red",
    9: "Orange",
    10: "Yellow",
    11: "Spring Green",
    12: "Green",
    13: "Turquoise",
}

while True:
    print("===============================================================")
    color_num = Mini1.I2C1.getColorNumber()
    print("color number=", color_dict[color_num])
    time.sleep(0.5)
