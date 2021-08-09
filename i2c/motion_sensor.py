class MotionSensor:
    def __init__(self, i2c_port, dev):
        self.i2c_port = i2c_port
        self.dev = dev

    def _complement(self, _buff):
        if len(str(_buff)) > 1:
            if _buff > 32767:
                _buff -= 65536
        return _buff

    def setFilter(self, filter_type):
        # Filter Optoins: "NONE", "GYRO", "CPLTY" , "KALMAN"
        filter_dict = {"NONE": 0, "GYRO": 1, "CPLTY": 2, "KALMAN": 3}
        if self.dev.board_type == "Micro":
            raise ValueError("setAngle only works on MATRIX Mini")
        _filter_type = self.dev._txEncode(filter_dict[filter_type])
        _buff = "I2C{}_SETFILTER".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff], _filter_type)

    def getAccel(self, axis):
        # axis (str) options: "X", "Y" or "Z"
        if self.dev.board_type == "Micro":
            raise ValueError("setAngle only works on MATRIX Mini")
        _buff = "I2C{}_GETACCEL_{}".format(self.i2c_port, axis.upper())
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getRoll(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getROll only works on MATRIX Mini")
        _buff = "I2C{}_GETROLL".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getYaw(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getYaw only works on MATRIX Mini")
        _buff = "I2C{}_GETYAW".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()

        return self._complement(self.dev._rxbuff)

    def getPitch(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getPitch only works on MATRIX Mini")
        _buff = "I2C{}_GETPITCH".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getGyro(self, axis):
        # axis (str) options: "X", "Y" or "Z"
        if self.dev.board_type == "Micro":
            raise ValueError("getGyro only works on MATRIX Mini")
        _buff = "I2C{}_GETGYRO_{}".format(self.i2c_port, axis.upper())
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self._complement(self.dev._rxbuff)

    def getTemperature(self):
        if self.dev.board_type == "Micro":
            raise ValueError("getTemperature only works on MATRIX Mini")
        _buff = "I2C{}_GETTEMP".format(self.i2c_port)
        self.dev._sendbuff(self.dev.protocol[_buff])
        self.dev._readbuff()
        return self.dev._rxbuff
