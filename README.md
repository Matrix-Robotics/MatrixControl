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
from MatrixControl import Mini
from MatrixControl import Micro

device1 = Micro(0, 115200) # set the first Micro to device1 
                           # with index 0 as buad 115200

device2 = Mini(0, 115200)  # set the first Minin to device2 
                           # with index 0 as buad 115200

device1.setRC(1, 100) # set RCservo 1 to Angle 100
device2.setMotor(2, 90) # set Motor 1 to Speed 90
```

# CAUTION

Make sure Raspberry pi's buad rate is equal to your MatrixController's. (Default buad rate is 115200) 

## License

MIT

## Supported Targets

* For MATRIX Mini / MATRIX Micro

