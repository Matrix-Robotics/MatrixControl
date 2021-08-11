import time
import serial

try:
    from Protocol import MiniP, MicroP
except ModuleNotFoundError:
    from .Protocol import MiniP, MicroP
from i2c.color_sensor import ColorSensor
from i2c.motion_sensor import MotionSensor
from i2c.servo_extension import ServoExtension
from i2c.motor_extension import MotorExtension


class Device(object):
    def __init__(self, device_num, board_type, buad=115200, tout=0.1):
        """Using buad rate and tout to control Matrix Mini board.
        ...

        Parameters
        ----------
        borad_type : str 
             Options: "Mini" or "Micro"
        device_num : int
             Device number, eg: 0, 1, ...
        buad : int
            (optional): buad rate. Defaults to 115200.
        tout : float 
            (optional) Upper limit of time out, seconds. Defaults to 0.1.
        """

        self.board_type = board_type
        if self.board_type == "Mini":
            self.protocol = MiniP
            self.BOOT_WAIT = 4
            self._PORT_ADJUST = 1
            self._MAX_ENCODE = 255
            self._MOTOR_WAIT = 0
            self._PID = "0403:6015"
            self.A1 = self.Analog(self, 1)
            self.A2 = self.Analog(self, 2)
            self.A3 = self.Analog(self, 3)
            self.M1 = self.Motor(self, 1)
            self.M2 = self.Motor(self, 2)
            self.RC1 = self.RC(self, 1)
            self.RC2 = self.RC(self, 2)
            self.RC3 = self.RC(self, 3)
            self.RC4 = self.RC(self, 4)
            self.D1 = self.Digital(self, 1)
            self.D2 = self.Digital(self, 2)
            self.D3 = self.Digital(self, 3)
            self.D4 = self.Digital(self, 4)
            self.RGB1 = self.RGB(self, 1)
            self.RGB2 = self.RGB(self, 2)
            self.BTN1 = self.BTN(self, 1)
            self.BTN2 = self.BTN(self, 2)

        else:
            self.protocol = MicroP
            self.BOOT_WAIT = 0.5
            self._PORT_ADJUST = 0
            self._MAX_ENCODE = 180
            self._MOTOR_WAIT = 0.01
            self._PID = "0D28:0204"
            self.A1 = self.Analog(self, 1)
            self.A2 = self.Analog(self, 2)
            self.M1 = self.Motor(self, 1)
            self.M2 = self.Motor(self, 2)
            self.RC1 = self.RC(self, 1)
            self.RC2 = self.RC(self, 2)
            self.D1 = self.Digital(self, 1)
            self.D2 = self.Digital(self, 2)
            self.U1 = self.Uart(self, 1)
            self.U2 = self.Uart(self, 2)

        self.i2c_devices = {
            "ColorSensor": ColorSensor,
            "MotionSensor": MotionSensor,
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
                if port[2].startswith("USB VID:PID=" + self._PID):  # FIDI FT230XS
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
                UARTbuffer = self._port.readline()
                if len(UARTbuffer) > 1:
                    self._rxbuff = int(UARTbuffer.decode().rstrip("\r\n"), 16)
                else:
                    self._rxbuff = None

    def _txEncode(self, para):
        _para = int(para)
        if _para > self._MAX_ENCODE - self._PORT_ADJUST:
            return self._MAX_ENCODE
        elif _para < 0:
            raise IndexError(
                "Index out of range, "
                "param is an integer between 0 and {}".format(self._MAX_ENCODE)
            )
        else:
            return _para + self._PORT_ADJUST

    class Motor:
        """Set DC Motor Speed
        ...

        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        motor_port : int
            motor_port is corresponding with M1, M2 sockets on board.
        """

        def __init__(self, dev, motor_port=1):
            self.dev = dev
            self.motor_port = motor_port

        def set(self, pwm):
            """Set Motor with specific socket and speed.
            Args:
                pwm (int): Speed of motor.
            """
            if pwm < 0 and pwm > -101:
                _pwm = 255 - (~pwm - self.dev._PORT_ADJUST)
            elif pwm > -1 and pwm < 101:
                _pwm = pwm + self.dev._PORT_ADJUST
            else:
                _pwm = None
                raise IndexError(
                    "Index out of range, " "pwm is an integer between -101 to 101."
                )
            _buff = "M{}_SET".format(self.motor_port)
            self.dev._sendbuff(self.dev.protocol[_buff], _pwm)
            time.sleep(self.dev._MOTOR_WAIT)

    class RC:
        """Set RC Servo Angle
        ...

        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        rc_port : int
            rc_port is corresponding with RC1, RC2, ... sockets on board.
        """

        def __init__(self, dev, rc_port=1):
            self.dev = dev
            self.rc_port = rc_port

        def set(self, angle):
            """
            Args:
                angle (int): Angle of RC motor.
            """
            _angle = self.dev._txEncode(angle)
            _buff = "RC{}_SET".format(self.rc_port)
            self.dev._sendbuff(self.dev.protocol[_buff], _angle)

        def releaseRC(self):
            if self.board_type == "Mini":
                raise ValueError("releaseRC only works on MATRIX Micro")
            self.dev._sendbuff(MicroP.RCRLS_SET)

    class Digital:
        """Set & Get Digital
        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        digital_port : int
            digital_port is corresponding with D1, D2, ... sockets on board.
        """

        def __init__(self, dev, digital_port=1):
            self.dev = dev
            self.digital_port = digital_port

        def setDIG(self, logic):
            """
            Args:
                logic (int): logic is GPIO output, eithrt 0 or 1.
            """
            if self.board_type == "Micro":
                raise ValueError("setDIG only works on MATRIX Mini")

            _logic = self._txEncode(logic)
            _buff = "D{}_SET".format(self.digital_port)
            self.dev._sendbuff(self.dev.protocol[_buff], _logic)

        def getDIG(self):
            _buff = "D{}_GET".format(self.digital_port)
            self.dev._sendbuff(self.dev.protocol[_buff])
            self.dev._readbuff()
            return self.dev._rxbuff

    class RGB:
        """Set RGB LED
        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        light_port : int
            light_port is RGB LEDs on board.
        """

        def __init__(self, dev, light_port=1):
            self.dev = dev
            self.light_port = light_port

        def setRGB(self, pwmR, pwmG, pwmB):
            """
            Args:
                pwmR (int): 0~255.
                pwmG (int): 0~255.
                pwmB (int): 0~255.
            """
            if self.dev.board_type == "Micro":
                raise ValueError("setRGB only works on MATRIX Mini")

            _pwmR = self.dev._txEncode(pwmR)
            _pwmG = self.dev._txEncode(pwmG)
            _pwmB = self.dev._txEncode(pwmB)
            _r_buff = "RGB{}R_SET".format(self.light_port)
            _g_buff = "RGB{}G_SET".format(self.light_port)
            _b_buff = "RGB{}B_SET".format(self.light_port)
            self.dev._sendbuff(self.dev.protocol[_r_buff], _pwmR)
            self.dev._sendbuff(self.dev.protocol[_g_buff], _pwmG)
            self.dev._sendbuff(self.dev.protocol[_b_buff], _pwmB)

    class BTN:
        """Get Button
        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        light_port : int
            button_port is on board.
        """

        def __init__(self, dev, button_port=1):
            self.dev = dev
            self.button_port = button_port

        def get(self):
            if self.dev.board_type == "Micro":
                raise ValueError("getBTN only works on MATRIX Mini")

            _buff = "BTN{}_GET".format(self.button_port)
            self.dev._sendbuff(self.dev.protocol[_buff])

            self.dev._readbuff()
            return self.dev._rxbuff

    class Analog:
        """Analog Port.
        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        analog_port int: 
            analog_port is corresponding with A1, A2, ... sockets on board.
        """

        def __init__(self, dev, analog_port):
            self.dev = dev
            self.analog_port = analog_port

        def getANG(self):
            _buff = "A{}_GET".format(self.analog_port)
            self.dev._sendbuff(self.dev.protocol[_buff])
            self.dev._readbuff()
            return self.dev._rxbuff

        def getDIG(self):
            _buff = "A{}_D_GET".format(self.analog_port)
            self.dev._sendbuff(self.dev.protocol[_buff])
            self.dev._readbuff()
            return self.dev._rxbuff

    class Uart:
        """Get Uart Port.
        Parameters
        ----------
        dev : class 
            MatrixControl.Device class
        uart_port int: 
            Uart Port Number, eg: 0, 1, ...
        """

        def __init__(self, dev, ur_port):
            self.dev = dev
            self.ur_port = ur_port

        def get(self):
            if self.dev.board_type == "Mini":
                raise ValueError("getUR only works on MATRIX Micro")
            _buff = "URD{}_GET".format(self.ur_port)
            self.dev._sendbuff(self.dev.protocol[_buff])
            self.dev_readbuff()
            return self.dev._rxbuff

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
        try:
            setattr(
                self, "I2C{}".format(port_num), self.i2c_devices[device](port_num, self)
            )
        except KeyError:
            raise KeyError("Please Add " + str(device) + "into i2c_devices list")

