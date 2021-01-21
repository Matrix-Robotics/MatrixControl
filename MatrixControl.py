import serial
import MiniProtocol as MiniP
import MicroProtocol as MicroP
import time


class Mini:
    def __init__(self, num, buad=115200, tout=0.1):
        self.__rxbuff = ''
        self.__timeout = tout
        self.__num = num
        self.__findPort()
        self.__buad = buad
        self.__port = serial.Serial(self.portlist[self.__num], buad, timeout=tout)
        time.sleep(2)

    def setMOTOR(self, num, pwm):
        if pwm < 0 and pwm > -101:
            _pwm = 255-(~pwm-1)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm+1
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
        _angle = self.__txEncode(angle)

        if num == 1:
            self.__sendbuff(MiniP.RC1_SET, _angle)
        elif num == 2:
            self.__sendbuff(MiniP.RC2_SET, _angle)
        elif num == 3:
            self.__sendbuff(MiniP.RC3_SET, _angle)
        elif num == 4:
            self.__sendbuff(MiniP.RC4_SET, _angle)
        else:
            print('parameter error')
            return None

    def setDIG(self, num, logic):
        _logic = self.__txEncode(logic)

        if num == 1:
            self.__sendbuff(MiniP.D1_SET, _logic)
        elif num == 2:
            self.__sendbuff(MiniP.D2_SET, _logic)
        elif num == 3:
            self.__sendbuff(MiniP.D3_SET, _logic)
        elif num == 4:
            self.__sendbuff(MiniP.D4_SET, _logic)
        else:
            print('parameter error')
            return None

    def setRGB(self, num, pwmR, pwmG, pwmB):
        _pwmR = self.__txEncode(pwmR)
        _pwmG = self.__txEncode(pwmG)
        _pwmB = self.__txEncode(pwmB)

        if num == 1:
            self.__sendbuff(MiniP.RGB1R_SET, _pwmR)
            self.__sendbuff(MiniP.RGB1G_SET, _pwmG)
            self.__sendbuff(MiniP.RGB1B_SET, _pwmB)
        elif num == 2:
            self.__sendbuff(MiniP.RGB2R_SET, _pwmR)
            self.__sendbuff(MiniP.RGB2G_SET, _pwmG)
            self.__sendbuff(MiniP.RGB2B_SET, _pwmB)
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

    def RST(self):
        self.__port.close()
        self.__port = serial.Serial(self.portlist[self.__num], self.__buad, timeout=self.__timeout)
        time.sleep(2)

    def close(self):
        self.RST()
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

    def __txEncode(self, para):
        _para = int(para)
        if _para > 254:
            return 255
        elif _para < 0:
            print('parameter error')
            return None
        else:
            return _para+1


class Micro:
    def __init__(self, num, buad=115200, tout=0.1):
        self.__rxbuff = ''
        self.__timeout = tout
        self.__num = num
        self.__findPort()
        self.__buad = buad
        self.__port = serial.Serial(self.portlist[self.__num], buad, timeout=tout)
        time.sleep(0.5)

    def setMOTOR(self, num, pwm):
        if pwm < 0 and pwm > -100:
            _pwm = 255-(~pwm)
        elif pwm > -1 and pwm < 100:
            _pwm = pwm
        else:
            _pwm = None
            print('parameter error')
        if num == 1:
            self.__sendbuff(MicroP.M1_SET, _pwm)
            time.sleep(0.01)
        elif num == 2:
            self.__sendbuff(MicroP.M2_SET, _pwm)
            time.sleep(0.01)
        else:
            print('parameter error')
            return None

    def setRC(self, num, angle):
        _angle = self.__txEncode(angle)

        if num == 1:
            self.__sendbuff(MicroP.RC1_SET, _angle)
        elif num == 2:
            self.__sendbuff(MicroP.RC2_SET, _angle)
        else:
            print('parameter error')
            return None

    def releaseRC(self):
        self.__sendbuff(MicroP.RCRLS_SET)

    def getDIG(self, num):
        if num == 1:
            self.__sendbuff(MicroP.D1_GET)
        elif num == 2:
            self.__sendbuff(MicroP.D2_GET)
        else:
            print('parameter error')
            return None
        self.__readbuff()
        return self.__rxbuff

    def getANG(self, num):
        if num == 1:
            self.__sendbuff(MicroP.A1_GET)
        elif num == 2:
            self.__sendbuff(MicroP.A2_GET)
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

    def __findPort(self):
        # Find first available microbit by searching USB ports.
        # Return serial port object.
        try:
            from serial.tools.list_ports import comports
        except ImportError:
            return None
        if comports:
            com_ports_list = list(comports())
            micro_port = []
            for port in com_ports_list:
                if port[2].startswith("USB VID:PID=0D28:0204"):  # Microbit
                    micro_port.append(port[0])
            self.portlist = micro_port

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
                self.__rxbuff = self.__port.readline().decode().rstrip("\r\n")

    def __txEncode(self, para):
        _para = int(para)
        if _para > 254:
            return 255
        elif _para < 0:
            print('parameter error')
            return None
        else:
            return _para+1
