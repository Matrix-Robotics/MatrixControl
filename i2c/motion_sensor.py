class MotionSensor:
    def __init__(self, i2c_port, dev):
        self.i2c_port = i2c_port
        self.dev = dev

    def _complement(self, _buff):
        if len(str(_buff)) > 1:
            if _buff > 32767:
                _buff -= 65536
        return _buff

    def getAccel(self, axis):
        # axis (str) options: "X", "Y" or "Z"
        _buff = "I2C{}_GETACCEL_{}".format(self.i2c_port, axis.upper())
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getRoll(self):
        _buff = "I2C{}_GETROLL".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getYaw(self):
        _buff = "I2C{}_GETYAW".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()

        return self._complement(self.dev._rxbuff)

    def getPitch(self):
        _buff = "I2C{}_GETPITCH".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getGyro(self, axis):
        # axis (str) options: "X", "Y" or "Z"
        _buff = "I2C{}_GETGYRO_{}".format(self.i2c_port, axis.upper())
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)
