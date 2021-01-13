import time
from MatrixControl import Mini

device1 = Mini(0, 115200)
t = 0.5
limit = 100
step = 5


try:
    while True:
        # for i in range(0, limit, step):
        #     device1.setRGB(1, i, 0, limit-i)
        #     device1.setRGB(2, i, 0, limit-i)
        #     time.sleep(t)
        # for i in range(0, limit, step):
        #     device1.setRGB(1, limit-i, i, 0)
        #     device1.setRGB(2, limit-i, i, 0)
        #     time.sleep(t)
        # for i in range(0, limit, step):
        #     device1.setRGB(1, 0, limit-i, i)
        #     device1.setRGB(2, 0, limit-i, i)
        #     time.sleep(t)

        # print("BTN1:", device1.getBTN(1))
        # print("BTN2:", device1.getBTN(2))

        # print("D1:", device1.getDIG(1))
        # print("D2:", device1.getDIG(2))
        # print("D3:", device1.getDIG(3))
        # print("D4:", device1.getDIG(4))

        # print("A1:", device1.getANG(1))
        # print("A2:", device1.getANG(2))
        # print("A3:", device1.getANG(4))

        time.sleep(t)

except KeyboardInterrupt:
    device1.close()
    print('DeviceClose')
