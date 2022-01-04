class LaserSensor:
    """Get rangefinder data by using LaserSensor.
    See [MatrixLaserSensor](https://matrix-robotics.github.io/MatrixLaserSensor/) for more details.

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

    # def _complement(self, _buff):
    #     if len(str(_buff)) > 1:
    #         if _buff > 32767:
    #             _buff -= 65536
    #     return _buff

    def getDistance(self):
        _buff = "I2C{}_GETDIS".format(self.i2c_port)
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        # return self._complement(self._dev._rxbuff)
        return self._dev._readbuff
