import time
import serial
import MiniProtocol as MiniP
import MicroProtocol as MicroP

class BoardControl:
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
        self.__port = serial.Serial(self.portlist[self.__device_num], buad, timeout=tout)
        # Wait n sec for device to boot.
        time.sleep(self.BOOT_WAIT)

    def __findPort(self):
        # Find first available FIDI by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            raise ImportError('Please install requirements.')
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

    def __sendbuff(self, func_name:str, para:int):
        """
        Args:
            func_name (str): Send buff via calling function name.
            para (int): Corresponding value of function.
        """
        if para is None:
            raise TypeError('Second parameter should be integer, not None.')
        self.__port.write((func_name + self.__dex2str(para) + "\n").encode())
    
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
            raise IndexError('Index out of range, '
                'param is an integer between 0 and {}'.format(self.MAX_ENCODE))
            return None

    def setMOTOR(self, motor_port, pwm):
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
            _pwm = None
            raise IndexError('Index out of range, '
                'pwm is an integer between -101 to 101.')
        
        if motor_port in (1, 2):
            _buff = "{}.M{}_SET".format(self.protocol, motor_port)
            self.__sendbuff(eval(_buff), _pwm)
            time.sleep(self.MOTOR_WAIT)
        else:
            raise IndexError('Index out of range, motor_port options: 1 or 2.')
            return None

    def setRC(self, rc_port, angle):
        """
        Args:
            rc_port (int)
            angle (int)
        """
        _angle = self.__txEncode(angle)
        _buff = "{}.RC{}_SET".format(self.protocol, rc_port)

        if self.board_type == 'Mini' and rc_port in range(1, 5):
            self.__sendbuff(eval(_buff), _angle)

        elif self.board_type == 'Micro' and rc_port in range(1, 3):
            self.__sendbuff(eval(_buff), _angle)
        else:
            raise IndexError('rc_port out of range, '
                'MATRIX Mini digital_port is an integer from 1 to 4.'
                'MATRIX Micro digital_port is an integer from 1 to 2.')
            return None

    def releaseRC(self):
        if self.board_type == 'Mini':
            raise ValueError('releaseRC only works on MATRIX Micro')
        self.__sendbuff(MicroP.RCRLS_SET)

    ##!!## TODO: protocal of Mini haven't be set yet.
    def setDIG(self, digital_port, logic):
        """
        Args:
            digital_port (int)
            logic (int)
        """
        # logic is 0 or 1
        if self.board_type == 'Micro':
            raise ValueError('setDIG only works on MATRIX Mini')

        _logic = self.__txEncode(logic)
        if digital_port in range(1, 5):
            _buff = "{}.D{}_SET".format(self.protocol, digital_port)
            self.__sendbuff(eval(_buff), _logic)
        else:
            raise IndexError('digital_port out of range, '
                'MATRIX Mini digital_port is an integer from 1 to 4.')
            return None

    def getDIG(self, digital_port):
        _buff = "{}.D{}_GET".format(self.protocol, digital_port)
        if self.board_type == 'Mini' and digital_port in range(1, 5):
            self.__sendbuff(eval(_buff))
        elif self.board_type == 'Micro' and digital_port in range(1, 3):
            self.__sendbuff(eval(_buff))
        else:
            raise IndexError('digital_port out of range, '
                'MATRIX Mini  digital_port is an integer from 1 to 4.'
                'MATRIX Micro  digital_port is an integer from 1 to 2.')
            return None
        self.__readbuff()
        return self.__rxbuff

    def setRGB(self, light_port, pwmR, pwmG, pwmB):
        if self.board_type == 'Micro':
            raise ValueError('setRGB only works on MATRIX Mini')

        _pwmR = self.__txEncode(pwmR)
        _pwmG = self.__txEncode(pwmG)
        _pwmB = self.__txEncode(pwmB)

        if light_port in range(1, 3):
            _buff = "{}.RGB{}_SET".format(self.protocol, light_port)
            self.__sendbuff(eval(_buff), _pwmR)
            self.__sendbuff(eval(_buff), _pwmG)
            self.__sendbuff(eval(_buff), _pwmB)
        else:
            raise IndexError('light_port out of range, '
                'MATRIX Mini light_port options: 1 or 2.')
            return None

    def getBTN(self, button_port):
        if self.board_type == 'Micro':
            raise ValueError('getBTN only works on MATRIX Mini')

        if button_port in range(1, 3):
            _buff = "{}.BTN{}_GET".format(self.protocol, button_port)
            self.__sendbuff(eval(_buff))
        else:
            raise IndexError('button_port out of range, '
                'MATRIX Mini button_port options: 1 or 2.')
            return None
        self.__readbuff()
        return self.__rxbuff

    def getANG(self, analog_port):
        _buff = "{}.A{}_GET".format(self.protocol, button_port)
        if device_type == 'Mini' and analog_port in range(1, 4):
            self.__sendbuff(eval(_buff))
        elif device_type == 'Micro' and analog_port in range(1, 3):
            self.__sendbuff(eval(_buff))
        else:
            raise IndexError('analog_port out of range, '
                'MATRIX Mini analog_port is an integer from 1 to 3; '
                'MATRIX Micro analog_port is from 1 to 2.')
            return None
        self.__readbuff()
        return self.__rxbuff
    
    def getUR(self, ur_port):
        if self.board_type == 'Mini':
            raise ValueError('getUR only works on MATRIX Micro')

        _buff = "{}.URD{}_GET".format(self.protocol, button_port)
        if ur_port in range(1, 3):
            self.__sendbuff(_buff)
        else:
            raise IndexError('ur_port out of range, '
                'MATRIX Micro ur_port is from 1 to 2.')
            return None
        self.__readbuff()
        return self.__rxbuff
    
    def RST(self):
        self.__port.close()
        self.__port = serial.Serial(self.portlist[self.__device_num], self.__buad, timeout=self.__timeout)
        time.sleep(2)

    def close(self):
        self.RST()
        self.__port.close()