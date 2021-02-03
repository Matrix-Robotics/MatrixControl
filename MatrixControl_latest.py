import time
import serial
import MiniProtocol as MiniP
import MicroProtocol as MicroP

class BoardControl:
    def __init__(self, board_type, device_num, buad=115200, tout=0.1):
        """Using buad rate and tout to control Matrix Mini board.
        Args:
            borad_type (str): options: "Mini" or "Micro"
            num (int): Device number, eg: 0, 1, ...
            buad (int, optional): [buad rate]. Defaults to 115200.
            tout (float, optional): [Upper limit of time out, seconds]. 
                Defaults to 0.1.
        """
        self.board_type = board_type
        if self.board_type == 'Mini':
            self.protocol = "MiniP"
            self.PORT_ADJUST = 1
            self.MAX_ENCODE = 255
            self.BOOT_WAIT = 2
            self.MOTOR_WAIT = 0
            self.PID = "0403:6015"
        else:
            self.protocol = "MicroP"
            self.PORT_ADJUST = 0
            self.MAX_ENCODE = 180
            self.BOOT_WAIT = 0.5
            self.MOTOR_WAIT = 0.01
            self.PID = "0D28:0204"

        # rxbuff: recieve buffer
        self.__rxbuff = ''
        self.__timeout = tout
        self.__device_num = device_num
        self.__findPort()
        self.__buad = buad
        self.__port = serial.Serial(self.portlist[self.__num], buad, timeout=tout)
        # Wait n sec for device to boot.
        time.sleep(self.BOOT_WAIT)

    def __findPort(self):
        # Find first available FIDI by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            com_ports_list = list(comports())
            _port_list = []
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID="+self.PID):  # FIDI FT230XS
                    _port_list.append(port[0])
            self.portlist = _port_list
    
    def __dex2str(self, dex):
        if dex < 0:
            return ""
        elif dex <= 15:
            return "0"+str(hex(dex+1).lstrip("0x"))
        else:
            return str(hex(dex).lstrip("0x"))

    def __sendbuff(self, func, para=-1):
        # TODO: Need to add exception
        self.__port.write((func + self.__dex2str(para) + "\n").encode())
    
    def __readbuff(self):
        tic = time.time()
        while ((time.time() - tic) < self.__timeout):
            while self.__port.in_waiting:
                self.__rxbuff = self.__port.readline().decode().rstrip("\r\n")

    def __txEncode(self, para):
        _para = int(para)
        
        if _para in range(0, self.MAX_ENCODE):
            return _para + self.PORT_ADJUST
        elif _para >= self.MAX_ENCODE:
            return self.MAX_ENCODE
        else:
            print('parameter error')
            return None
    
    def register(self, *device_type):
        pass

    def setMOTOR(self, motor_port:int, pwm:int):
        """ Set Motor with specific socket and speed.
        Args:
            motor_port (int): 
                motor_port is corresponding with M1, M2 socket on board.
            pwm (int): Speed of motor.
        """

        if pwm < 0 and pwm > -101:
            _pwm = 255-(~pwm - self.PORT_ADJUST)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm + self.PORT_ADJUST
        else:
            # TODO break point
            _pwm = None
            print('pwm is an integer between -101 to 101.')
        
        if motor_port in (1, 2):
            _buff = "{}.M{}_SET".format(self.protocol, motor_port)
            self.__sendbuff(eval(_buff), _pwm)
            time.sleep(self.MOTOR_WAIT)
        else:
            print('motor_port options: 1 or 2 .')
            return None

    def setRC(self, rc_port:int, angle:int):
        _angle = self.__txEncode(angle)
        _buff = "{}.RC{}_SET".format(self.protocol, rc_port)

        if self.board_type == 'Mini' and rc_port in range(1, 5):
            self.__sendbuff(eval(_buff), _angle)

        elif self.board_type == 'Micro' and rc_port in range(1, 3):
            self.__sendbuff(eval(_buff), _angle)
        else:
            return None

    def releaseRC(self):
        # TODO Only works on MATRIX Micro
        self.__sendbuff(MicroP.RCRLS_SET)

    def setDIG(self, digital_port:int, logic:int):
        # logic is 0 or 1
        # TODO Only works on MATRIX Mini
        _logic = self.__txEncode(logic)
        if digital_port in range(1, 5):
            _buff = "{}.D{}_SET".format(self.protocol, digital_port)
            self.__sendbuff(eval(_buff), _logic)
        else:
            print('digital_port out of range')
            return None

    def getDIG(self, digital_port):
        if digital_port in range(1, 5):
            _buff = "{}.D{}_GET".format(self.protocol, digital_port)
            self.__sendbuff(eval(_buff))
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def setRGB(self, light_port, pwmR, pwmG, pwmB):
        # Only works on MATRIX Mini
        _pwmR = self.__txEncode(pwmR)
        _pwmG = self.__txEncode(pwmG)
        _pwmB = self.__txEncode(pwmB)

        if light_port in range(1, 3):
            _buff = "{}.RGB{}_SET".format(self.protocol, light_port)
            self.__sendbuff(eval(_buff), _pwmR)
            self.__sendbuff(eval(_buff), _pwmG)
            self.__sendbuff(eval(_buff), _pwmB)
        else:
            print('light_port out of range')
            return None

    def getBTN(self, button_port):
        # Only works on MATRIX Mini
        if button_port in range(1, 3):
            _buff = "{}.BTN{}_GET".format(self.protocol, button_port)
            self.__sendbuff(eval(_buff))
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def getANG(self, analog_port):
        _buff = "{}.A{}_GET".format(self.protocol, button_port)
        if device_type == 'Mini' and analog_port in range(0, 4):
            self.__sendbuff(eval(_buff))
        elif device_type == 'Micro' and analog_port in range(0, 3):
            self.__sendbuff(eval(_buff))
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff
    
    def getUR(self, ur_port):
        # Only works on MATRIX Micro
        _buff = "{}.URD{}_GET".format(self.protocol, button_port)
        if ur_port in range(1, 3):
            self.__sendbuff(_buff)
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff
    
    def RST(self):
        self.__port.close()
        self.__port = serial.Serial(self.portlist[self.__num], self.__buad, timeout=self.__timeout)
        time.sleep(2)

    def close(self):
        self.RST()
        self.__port.close()


    