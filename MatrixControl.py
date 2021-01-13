import serial
import MiniProtocol as MiniP
import time


class Mini:
    def __init__(self, num, buad=115200, timeout=0.1):
        self.__rxbuff = ''
        self.__timeout = timeout
        self.__findPort()
        self.__port = serial.Serial(self.portlist[num], buad, timeout=timeout)
        time.sleep(2)

    def setMOTOR(self, num, pwm):
        if pwm < 0 and pwm > -101:
            _pwm = 255-(~pwm)
        elif pwm > 0 and pwm < 101:
            _pwm = pwm
        else:
            _pwm = None
            print('parameter error')
        if num == 1:
            self.__sendbuff(MiniP.M1_SET, _pwm)
        elif num == 2:
            self.__sendbuff(MiniP.M2_SET, _pwm)
        else:
            print('parameter error')
            return None

    def setRC(self, num, angle):
        if num == 1:
            self.__sendbuff(MiniP.RC1_SET, angle)
        elif num == 2:
            self.__sendbuff(MiniP.RC2_SET, angle)
        elif num == 3:
            self.__sendbuff(MiniP.RC3_SET, angle)
        elif num == 4:
            self.__sendbuff(MiniP.RC4_SET, angle)
        else:
            print('parameter error')
            return None

    def setDIG(self, num, logic):
        if num == 1:
            self.__sendbuff(MiniP.D1_SET, logic)
        elif num == 2:
            self.__sendbuff(MiniP.D2_SET, logic)
        elif num == 3:
            self.__sendbuff(MiniP.D3_SET, logic)
        elif num == 4:
            self.__sendbuff(MiniP.D4_SET, logic)
        else:
            print('parameter error')
            return None

    def setRGB(self, num, pwmR, pwmG, pwmB):
        if num == 1:
            self.__sendbuff(MiniP.RGB1R_SET, pwmR)
            self.__sendbuff(MiniP.RGB1G_SET, pwmG)
            self.__sendbuff(MiniP.RGB1B_SET, pwmB)
        elif num == 2:
            self.__sendbuff(MiniP.RGB2R_SET, pwmR)
            self.__sendbuff(MiniP.RGB2G_SET, pwmG)
            self.__sendbuff(MiniP.RGB2B_SET, pwmB)
        else:
            print('parameter error')
            return None

    def getBTN(self, num):
        if num == 1:
            self.__sendbuff(MiniP.BTN1_GET)
        elif num == 2:
            self.__sendbuff(MiniP.BTN2_GET)
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def getDIG(self, num):
        if num == 1:
            self.__sendbuff(MiniP.D1_GET)
        elif num == 2:
            self.__sendbuff(MiniP.D2_GET)
        elif num == 3:
            self.__sendbuff(MiniP.D3_GET)
        elif num == 4:
            self.__sendbuff(MiniP.D4_GET)
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def getANG(self, num):
        if num == 1:
            self.__sendbuff(MiniP.A1_GET)
        elif num == 2:
            self.__sendbuff(MiniP.A2_GET)
        elif num == 3:
            self.__sendbuff(MiniP.A3_GET)
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def close(self):
        self.__port.close()

    def __findPort(self):
        # Find first available FIDI by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            com_ports_list = list(comports())
            fidi_port = []
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=0403:6015"):  # FIDI FT230XS
                    fidi_port.append(port[0])
            self.portlist = fidi_port

    def __dex2str(self, dex):
        if dex < 0:
            return ""
        elif dex <= 15:
            return "0"+str(hex(dex+1).lstrip("0x"))
        else:
            return str(hex(dex).lstrip("0x"))

    def __sendbuff(self, func, para=-1):
        self.__port.write((func + self.__dex2str(para) + "\n").encode())

    def __readbuff(self):
        tic = time.time()
        while ((time.time() - tic) < self.__timeout):
            while self.__port.in_waiting:
                self.__rxbuff = int(self.__port.readline().decode().rstrip("\r\n"), 16)
