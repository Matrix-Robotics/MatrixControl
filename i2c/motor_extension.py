class MotorExtension:
    def setPWM(self, channel, pwm):
        # channel options: from 1 to 8
        if self.dev.board_type == "Micro":
            raise ValueError("setAngle only works on MATRIX Mini")
        _angle = self.dev._txEncode(pwm)
        _buff = "I2C{}_SETPWM_CH{}".format(self.i2c_port, channel)
        self.dev._sendbuff(self.dev.protocol[_buff], _angle)
        self.dev._readbuff()
        return self.dev._rxbuff
