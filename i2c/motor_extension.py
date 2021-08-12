class MotorExtension:
    def __init__(self, i2c_port, dev):
        self.i2c_port = i2c_port
        self.dev = dev

    def setPWM(self, channel, pwm):
        # channel options: from 1 to 8
        # pwm (int): from -255 to 255
        _angle = self.dev._txEncode(pwm)
        _buff = "I2C{}_SETPWM_CH{}".format(self.i2c_port, channel)
        self.dev._sendbuff(self.dev.protocol[_buff], _angle)
