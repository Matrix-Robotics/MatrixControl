# MatrixControl
Control API for any MATRIX controller base on python.

## Getting Started

Notice: Support Python 3.5 and above.

### Step 1: Install Requirements

```shell
$ git clone https://github.com/Matrix-Robotics/MatrixControl.git
$ cd MatrixControl
$ pip install -r requirements.txt
```
You can use MatrixControl library to control any MATRIX controller via any device which runs python.

### Step 2: Connect via your device

- On MATRIX Mini
  * Turn on power button
  * Connect MATRIX Mini and host via USB Type B
 
- On MATRIX Micro
  * Micobit Plug into MATRIX Micro
  * Turn on power button
  * Connect MATRIX Micro and host device via Micro USB

### Enable MatrixControl on device
- On MATRIX Mini
  * start enable block before other blocks and select the buad

![image](https://github.com/Matrix-Robotics/MatrixControl/blob/main/doc/pic/Enable_MATRIX_Mini.png)

- On MATRIX Micro
  * Put enable block to on start stage and select the buad

![image](https://github.com/Matrix-Robotics/MatrixControl/blob/main/doc/pic/Enable_MATRIX_Micro.png)

## Basic Usage

```python
import time
from MatrixControl import Device

Mini1 = Device(0, "Mini")

t = 1
limit = 100
step = 5

try:
    while True:
        # get Button click, 1 means true, 0 means false
        print("BTN1:", Mini1.BTN1.get())
        print("BTN2:", Mini1.BTN2.get())
        # get Analog data
        print("A1 ANG:", Mini1.A1.getANG())
        print("A2 ANG:", Mini1.A2.getANG())
        print("A3 ANG:", Mini1.A3.getANG())
        # get Digital data
        print("D1 DIG:", Mini1.D1.getDIG())
        print("D2 DIG:", Mini1.D2.getDIG())
        print("D3 DIG:", Mini1.D3.getDIG())

        # set Motor speed
        Mini1.M1.set(50)
        Mini1.M2.set(50)
        # set RGB LED
        Mini1.RGB1.setRGB(0, 0, 255)
        Mini1.RGB2.setRGB(0, 0, 0)
        time.sleep(t)

        Mini1.M1.set(-50)
        Mini1.M2.set(-50)
        Mini1.RGB1.setRGB(0, 0, 0)
        Mini1.RGB2.setRGB(0, 0, 255)
        time.sleep(t)
        print("=========================")

except KeyboardInterrupt:
    Mini1.close()
    print("DeviceClose")
```
# I2C Devices
Checkout [**examples**](./examples) for more information.

# CAUTION

Make sure master device buad rate is equal to your MatrixController's. (Default buad rate is 115200) 

## License

MIT

## Supported Targets

* For MATRIX Mini / MATRIX Micro

