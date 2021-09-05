class ServoExtension:
    """Set RC Motor Speed by using ServoExtension.
    See [MatrixServoExtension](https://matrix-robotics.github.io/MatrixServoExtension/) for more details.
    
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

    def setAngle(self, channel, angle):
        """Set RC Motor Speed by using ServoExtension.

        Parameters
        ----------
        angle : int
            angle is from 0 to 180.
        channel : int 
            channel is from 1 to 8.
        """
        _angle = self._dev._txEncode(angle)
        _buff = "I2C{}_SETANGLE_CH{}".format(self.i2c_port, channel)
        self._dev._sendbuff(self._dev.protocol[_buff], _angle)
