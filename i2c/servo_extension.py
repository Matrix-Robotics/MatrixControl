class ServoExtension:
    def __init__(self, i2c_port, dev):
        self.i2c_port = i2c_port
        self.dev = dev

    def setAngle(self, channel, angle):
        # channel options: from 1 to 8
        _angle = self.dev._txEncode(angle)
        _buff = "I2C{}_SETANGLE_CH{}".format(self.i2c_port, channel)
        self.dev._sendbuff(self.dev.protocol[_buff], _angle)
        self.dev._readbuff()
        return self.dev._rxbuff

    def ChannelRelease(self, channel):
        # channel options: from 1 to 8
        if self.dev.board_type == "Micro":
            raise ValueError("ChannelRelease only works on MATRIX Mini")

        _buff = "I2C{}_CHRELEASE_CH{}".format(self.i2c_port, channel)
        self.dev._sendbuff(self.dev.protocol[_buff], 1)
        self.dev._readbuff()
        return self.dev._rxbuff
