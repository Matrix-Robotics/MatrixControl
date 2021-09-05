import math
import time


def mapData(x):
    # map input from -255~255 to -100~100
    y = (x + 255) / 512 * 200 - 100
    return math.ceil(y)


class MotorExtension:
    """Set DC Motor Speed by using MotorExtension.
    See [MatrixMotionSensor](https://matrix-robotics.github.io/MatrixMotionSensor/) for more details.

    Parameters
    ----------
    i2c_port : int
        i2c_port is corresponding with I2C1, I2C2 ... sockets on board.
    _dev : class 
        MatrixControl.Device class
    """

    def __init__(self, _dev, i2c_port):
        self.i2c_port = i2c_port
        self._dev = _dev
        # wait device boot
        time.sleep(6)

    def setPWM(self, channel, pwm):
        """Set RC Motor Speed by using ServoExtension.

        Parameters
        ----------
        
        channel : int 
            channel is from 1 to 4.
        pwm : int
            pwm is from -255 to 255.
        """
        pwm = mapData(pwm)
        if pwm < 0 and pwm > -101:
            _pwm = 255 - (~pwm - 1)
        elif pwm > -1 and pwm < 101:
            _pwm = pwm + 1
        else:
            _pwm = None
            raise IndexError(
                "Index out of range, " "pwm is an integer between -255 to 255."
            )
        _buff = "I2C{}_SETPWM_CH{}".format(self.i2c_port, channel)
        self._dev._sendbuff(self._dev.protocol[_buff], _pwm)
