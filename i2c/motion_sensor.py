class MotionSensor:
    """Get 9Dof data by using MotionSensor.
    See [MatrixMotionSensor](https://matrix-robotics.github.io/MatrixMotionSensor/) for more details.

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

    def _complement(self, _buff):
        if len(str(_buff)) > 1:
            if _buff > 32767:
                _buff -= 65536
        return _buff

    def getAccel(self, axis):
        """Get Accel Data. (unit: mm/s^2)

        Parameters
        ----------
        axis : str
            options are "X", "Y" or "Z"
        """
        _buff = "I2C{}_GETACCEL_{}".format(self.i2c_port, axis.upper())
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        return self._complement(self._dev._rxbuff)

    def getGyro(self, axis):
        """Get Gyro Data. (unit: degree per second)

        Parameters
        ----------
        axis : str
            options are "X", "Y" or "Z"
        """
        _buff = "I2C{}_GETGYRO_{}".format(self.i2c_port, axis.upper())
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        return self._complement(self._dev._rxbuff)

    def getRoll(self):
        _buff = "I2C{}_GETROLL".format(self.i2c_port)
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        return self._complement(self._dev._rxbuff)

    def getYaw(self):
        _buff = "I2C{}_GETYAW".format(self.i2c_port)
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()

        return self._complement(self._dev._rxbuff)

    def getPitch(self):
        _buff = "I2C{}_GETPITCH".format(self.i2c_port)
        self._dev._sendbuff(self._dev.protocol[_buff])
        self._dev._readbuff()
        return self._complement(self._dev._rxbuff)

