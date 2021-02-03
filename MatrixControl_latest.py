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
            self.protocol = MiniP
        else:
            self.protocol = MicroP
        # rxbuff: recieve buffer
        self.__rxbuff = ''
        self.__timeout = tout
        self.__device_num = device_num
        self.__findPort()
        self.__buad = buad
        self.__port = serial.Serial(self.portlist[self.__num], buad, timeout=tout)
        # Wait 2 sec for Mini to boot.
        # TODO
        time.sleep(2)

    def register(self, *device_type):
        pass

    def __sendbuff(self, func, para=-1):
        # TODO: Need to add exception
        self.__port.write((func + self.__dex2str(para) + "\n").encode())

    def setMOTOR(self, motor_num:int, pwm:int):
        """ Set Motor with specific socket and speed.
        Args:
            motor_num (int): 
                motor_num is corresponding with M1, M2 socket on board.
            pwm (int): Speed of motor.
        """

        if self.board_type == 'Mini':
            pwm_adjust = 1
        else:
            # Micro
            pwm_adjust = 0

        if pwm < 0 and pwm > -101:
            _pwm = 255-(~pwm-pwm_adjust)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm+pwm_adjust
        else:
            # TODO break point
            _pwm = None
            print('pwm is an integer between -101 to 101.')
        
        if motor_num in (1, 2):
            _buff = "{}.M{}_SET".format(self.protocol, motor_num)
            self.__sendbuff(eval(_buff), _pwm)
        else:
            print('motor_num options: 1 or 2 .')
            return None

    def setRC(self, rc_num, angle):
        _angle = self.__txEncode(angle)
        _buff = "{}.RC{}_SET".format(self.protocol, rc_num)

        if self.board_type == 'Mini' and rc_num in range(1, 5):
            self.__sendbuff(eval(_buff), _angle)

        elif self.board_type == 'Micro' and rc_num in (1, 2):
            self.__sendbuff(eval(_buff), _angle)
        else:
            return None
    
