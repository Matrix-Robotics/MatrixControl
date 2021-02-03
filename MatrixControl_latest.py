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
        time.sleep(2)

    def register(self, *device_type):
        pass

    def setMOTOR(self, motor_num:int, pwm:int):
        if self.board_type == 'Mini':
            pwm_adjust = 1
        else:
            # Mico
            pwm_adjust = 0

        if pwm < 0 and pwm > -101:
            _pwm = 255-(~pwm-pwm_adjust)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm+pwm_adjust
        else:
            _pwm = None
            print('pwm is an integer between -101 to 101.')

        if motor_num == 1:
            self.__sendbuff(MiniP.M1_SET, _pwm)
        elif motor_num == 2:
            self.__sendbuff(MiniP.M2_SET, _pwm)
        else:
            print('motor_num option: 1 or 2')
            return None

    
