class ColorSensor:
    """Set Color Data by using ColorSensor.
    See [MatrixColorSensor](https://matrix-robotics.github.io/MatrixColorSensor/) for more details.    
    
    Parameters
    ----------
    i2c_port : int
        i2c_port is corresponding with I2C1, I2C2 ... sockets on board.
    _dev : class 
        MatrixControl.Device class
    """

    def __init__(self, _dev, i2c_port):
        self.i2c_port = i2c_port
        self._dev = _dev
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
        """
        Parameters
        ----------
        color : str
            color options: R, G, B, C, M, Y, K
        """
        if color not in self.color_options:
            raise KeyError("Color Options: R, G, B, C, M, Y, K")
        _buff = "I2C{}_GET_COLOR{}".format(self.i2c_port, color.upper())
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        return self._dev._rxbuff

    def getColorNumber(self):
        _buff = "I2C{}_GET_COLORNUMBER".format(self.i2c_port)
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        if self._dev._rxbuff in self.color_dict.keys():
            return self.color_dict[self._dev._rxbuff]
        return ""
