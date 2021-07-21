import time
import sys, os

sys.path.insert(0, os.path.abspath("../.."))
from MatrixControl import Device

Mini1 = Device(0, "Mini", 115200)

while True:
    print("===============================================================")

    channel = 1
    pwm = 255
    Mini1.I2C1.setPWM(channel, pwm)
    print("set channel " + str(channel) + " to " + str(pwm))
    time.sleep(0.5)

    channel = 2
    pwm = -255
    Mini1.I2C1.setPWM(channel, pwm)
    print("set channel " + str(channel) + " to " + str(pwm))
    time.sleep(0.5)

    channel = 1
    pwm = -255
    Mini1.I2C1.setPWM(channel, pwm)
    print("set channel " + str(channel) + " to " + str(pwm))
    time.sleep(0.5)

    channel = 2
    pwm = 255
    Mini1.I2C1.setPWM(channel, pwm)
    print("set channel " + str(channel) + " to " + str(pwm))
    time.sleep(0.5)
