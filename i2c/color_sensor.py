class ColorSensor:
    def __init__(self, i2c_port, dev):
        self.i2c_port = i2c_port
        self.dev = dev
        self.color_options = ["R", "G", "B", "C", "M", "Y", "K"]
        self.color_dict = {
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

    def getColor(self, color):
        # color options: R, G, B, C, M, Y, K
        if color not in self.color_options:
            raise KeyError("Color Options: R, G, B, C, M, Y, K")
        _buff = "I2C{}_GET_COLOR{}".format(self.i2c_port, color.upper())
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self.dev._rxbuff

    def getColorNumber(self):
        _buff = "I2C{}_GET_COLORNUMBER".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        if self.dev._rxbuff in self.color_dict.keys():
            return self.color_dict[self.dev._rxbuff]
        return ""
