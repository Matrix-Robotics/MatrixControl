import sys
sys.path.insert(1, "../")

import time
from MatrixControl import BoardControl
# from MatrixControl import Mini

class RobotControl():
    def __init__(self):
        self.device = BoardControl(0, "Mini")
        # self.device = Mini(0)

        self.limit = 100
        self.step = 5

    def walk_forward(self, t=None):
        self.device.setMOTOR(1, 100)
        self.device.setMOTOR(2, 100)
        if t:
            time.sleep(t)
            self.device.setMOTOR(1, 0)
            self.device.setMOTOR(2, 0)

    def walk_backward(self, t=None):
        self.device.setMOTOR(1, -100)
        self.device.setMOTOR(2, -100)
        if t:
            time.sleep(t)
            self.device.setMOTOR(1, 0)
            self.device.setMOTOR(2, 0)

    def turn_right(self):
        self.device.setMOTOR(1, 100)
        time.sleep(0.5)
        self.device.setMOTOR(1, 0)

    def turn_left(self):
        self.device.setMOTOR(2, 100)
        time.sleep(0.5)
        self.device.setMOTOR(2, 0)

    def stop(self):
        self.device.setMOTOR(1, 0)
        self.device.setMOTOR(2, 0)

    
rc = RobotControl()

## Use Case

while True:
    c = input("Input direction:")

    if c == 'w':
        rc.walk_forward()
    elif c == 's':
        rc.walk_backward()
    elif c == 'a':
        rc.turn_left()
    elif c == 'd':
        rc.turn_right()
    elif c == 'z':
        rc.stop()

