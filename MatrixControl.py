import time
import serial

try:
    from Protocol import MiniP, MicroP
except ModuleNotFoundError:
    from .Protocol import MiniP, MicroP
from i2c.color_sensor import ColorSensor
from i2c.servo_extension import ServoExtension
from i2c.motor_extension import MotorExtension


class Device(object):
    def __init__(self, device_num, board_type, buad=115200, tout=0.1):
        """Using buad rate and tout to control Matrix Mini board.
        Args:
            borad_type (str): options: "Mini" or "Micro"
            device_num (int): Device number, eg: 0, 1, ...
            buad (int, optional): [buad rate]. Defaults to 115200.
            tout (float, optional): [Upper limit of time out, seconds].
            Defaults to 0.1.
        """

        self.board_type = board_type
        if self.board_type == "Mini":
            self.protocol = MiniP
            self.PORT_ADJUST = 1
            self.MAX_ENCODE = 255
            self.BOOT_WAIT = 4
            self.MOTOR_WAIT = 0
            self.PID = "0403:6015"
        else:
            self.protocol = MicroP
            self.PORT_ADJUST = 0
            self.MAX_ENCODE = 180
            self.BOOT_WAIT = 0.5
            self.MOTOR_WAIT = 0.01
            self.PID = "0D28:0204"

        self._i2c_devices = {
            "ColorSensor": ColorSensor,
            "ServoExtension": ServoExtension,
            "MotorExtension": MotorExtension,
        }

        # rxbuff: recieve buffer
        self._rxbuff = ""
        self._timeout = tout
        self._device_num = device_num
        self._findPort()
        self._buad = buad
        self._port = serial.Serial(self.portlist[self._device_num], buad, timeout=tout)
        # Wait n sec for device to boot.
        time.sleep(self.BOOT_WAIT)

    def _findPort(self):
        # Find first available FIDI by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            raise ImportError("Please install requirements.")

        if comports:
            com_ports_list = list(comports())
            _port_list = []
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=" + self.PID):  # FIDI FT230XS
                    _port_list.append(port[0])
            self.portlist = _port_list
            if len(self.portlist) == 0:
                raise RuntimeError(
                    "Cannot Read Device, please check your cable and device: {}. ".format(
                        self.board_type
                    )
                )

    def _dex2str(self, dex):
        if dex < 0:
            return ""
        elif dex <= 15:
            return "0" + str(hex(dex + 1).lstrip("0x"))
        else:
            return str(hex(dex).lstrip("0x"))

    def _sendbuff(self, func_name, para=-1):
        """
        Args:
            func_name (str): Send buff via calling function name.
            para (int): Corresponding value of function.
        """
        if para is None:
            raise TypeError("Second parameter should be integer, not None.")
        self._port.write((func_name + self._dex2str(para) + "\n").encode())

    def _readbuff(self):
        tic = time.time()
        while (time.time() - tic) < self._timeout:
            while self._port.in_waiting:
                self._rxbuff = int(self._port.readline().decode().rstrip("\r\n"), 16)

    def _txEncode(self, para):
        _para = int(para)
        if _para > self.MAX_ENCODE - self.PORT_ADJUST:
            return self.MAX_ENCODE
        elif _para < 0:
            raise IndexError(
                "Index out of range, "
                "param is an integer between 0 and {}".format(self.MAX_ENCODE)
            )
        else:
            return _para + self.PORT_ADJUST

    def setMOTOR(self, motor_port, pwm):
        """Set Motor with specific socket and speed.
        Args:
            motor_port (int):
                motor_port is corresponding with M1, M2 sockets on board.
            pwm (int): Speed of motor.
        """

        if pwm < 0 and pwm > -101:
            _pwm = 255 - (~pwm - self.PORT_ADJUST)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm + self.PORT_ADJUST
        else:
            _pwm = None
            raise IndexError(
                "Index out of range, " "pwm is an integer between -101 to 101."
            )

        if motor_port in (1, 2):
            _buff = "M{}_SET".format(motor_port)
            self._sendbuff(self.protocol[_buff], _pwm)
            time.sleep(self.MOTOR_WAIT)
        else:
            raise IndexError("Index out of range, motor_port options: 1 or 2.")

    def setRC(self, rc_port, angle):
        """
        Args:
            rc_port (int):
                rc_port is corresponding with RC1, RC2... sockets on board.
            angle (int): Angle of RC motor.
        """
        _angle = self._txEncode(angle)
        _buff = "RC{}_SET".format(rc_port)

        if self.board_type == "Mini" and rc_port in range(1, 5):
            self._sendbuff(self.protocol[_buff], _angle)

        elif self.board_type == "Micro" and rc_port in range(1, 3):
            self._sendbuff(self.protocol[_buff], _angle)
        else:
            raise IndexError(
                "rc_port out of range, "
                "MATRIX Mini digital_port is an integer from 1 to 4."
                "MATRIX Micro digital_port is an integer from 1 to 2."
            )

    def releaseRC(self):
        if self.board_type == "Mini":
            raise ValueError("releaseRC only works on MATRIX Micro")
        self._sendbuff(MicroP.RCRLS_SET)

    def setDIG(self, digital_port, logic):
        """
        Args:
            digital_port (int)
            logic (int): logic is GPIO output, eithrt 0 or 1.
        """
        if self.board_type == "Micro":
            raise ValueError("setDIG only works on MATRIX Mini")

        _logic = self._txEncode(logic)
        if digital_port in range(1, 5):
            _buff = "D{}_SET".format(digital_port)
            self._sendbuff(self.protocol[_buff], _logic)
        else:
            raise IndexError(
                "digital_port out of range, "
                "MATRIX Mini digital_port is an integer from 1 to 4."
            )

    def getDIG(self, digital_port):
        _buff = "D{}_GET".format(digital_port)
        if self.board_type == "Mini" and digital_port in range(1, 5):
            self._sendbuff(self.protocol[_buff])
        elif self.board_type == "Micro" and digital_port in range(1, 3):
            self._sendbuff(self.protocol[_buff])
        else:
            raise IndexError(
                "digital_port out of range, "
                "MATRIX Mini  digital_port is an integer from 1 to 4."
                "MATRIX Micro  digital_port is an integer from 1 to 2."
            )
        self._readbuff()
        return self._rxbuff

    def setRGB(self, light_port, pwmR, pwmG, pwmB):
        if self.board_type == "Micro":
            raise ValueError("setRGB only works on MATRIX Mini")

        _pwmR = self._txEncode(pwmR)
        _pwmG = self._txEncode(pwmG)
        _pwmB = self._txEncode(pwmB)
        if light_port in range(1, 3):
            _r_buff = "RGB{}R_SET".format(light_port)
            _g_buff = "RGB{}G_SET".format(light_port)
            _b_buff = "RGB{}B_SET".format(light_port)
            self._sendbuff(self.protocol[_r_buff], _pwmR)
            self._sendbuff(self.protocol[_g_buff], _pwmG)
            self._sendbuff(self.protocol[_b_buff], _pwmB)
        else:
            raise IndexError(
                "light_port out of range, MATRIX Mini light_port \
                    options: 1 or 2."
            )

    def getBTN(self, button_port):
        if self.board_type == "Micro":
            raise ValueError("getBTN only works on MATRIX Mini")

        if button_port in range(1, 3):
            _buff = "BTN{}_GET".format(button_port)
            self._sendbuff(self.protocol[_buff])
        else:
            raise IndexError("button_port out of range, button_port options: 1 or 2.")

        self._readbuff()
        return self._rxbuff

    def getANG(self, analog_port):
        _buff = "A{}_GET".format(analog_port)
        if self.board_type == "Mini" and analog_port in range(1, 4):
            self._sendbuff(self.protocol[_buff])
        elif self.board_type == "Micro" and analog_port in range(1, 3):
            self._sendbuff(self.protocol[_buff])
        else:
            raise IndexError(
                "analog_port out of range, "
                "MATRIX Mini analog_port is an integer from 1 to 3; "
                "MATRIX Micro analog_port is from 1 to 2."
            )
        self._readbuff()
        return self._rxbuff

    def getUR(self, ur_port):
        if self.board_type == "Mini":
            raise ValueError("getUR only works on MATRIX Micro")

        _buff = "URD{}_GET".format(ur_port)
        if ur_port in range(1, 3):
            self._sendbuff(self.protocol[_buff])
        else:
            raise IndexError("ur_port out of range, ur_port is from 1 to 2.")
        self._readbuff()
        return self._rxbuff

    def RST(self):
        self._port.close()
        self._port = serial.Serial(
            self.portlist[self._device_num], self._buad, timeout=self._timeout
        )
        time.sleep(2)

    def close(self):
        self.RST()
        self._port.close()

    def SetI2C(self, port_num, device):
        setattr(self, "I2C{}".format(port_num), self._i2c_devices[device](port_num, self))
