import servo_extension as SE
from MatrixControl import Device

class I2C(Device):
    def __init__(self, i2c_port, i2c_dev):
        self.i2c_port = i2c_port
        self.i2c_dev = i2c_dev

        self.setAngle = ServoExtension.setAngle
