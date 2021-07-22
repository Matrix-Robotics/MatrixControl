class ColorSensor:
    def getColor(self, color):
        # color options: R, G, B, C, M, Y, K
        if self.dev.board_type == "Micro":
            raise ValueError("getColor only works on MATRIX Mini")
        _buff = "I2C{}_GET_COLOR{}".format(self.i2c_port, color)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self.dev._rxbuff

    def getGrayscale(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getGrayscale only works on MATRIX Mini")
        _buff = "I2C{}_GET_GRAYSCALE".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self.dev._rxbuff

    def getColorNumber(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getColorNumber only works on MATRIX Mini")
        _buff = "I2C{}_GET_COLORNUMBER".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self.dev._rxbuff