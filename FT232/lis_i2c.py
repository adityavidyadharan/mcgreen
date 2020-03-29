import time
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
from micropython import const
import lis3dh_deplib

FT232H.use_FT232H()
ft232h = FT232H.FT232H(serial='black')
address = 0x18
lis3dh = lis3dh_deplib.LIS3DH_I2C(ft232h, address)
lis3dh.range = lis3dh_deplib.RANGE_2_G
lis3dh.data_rate = lis3dh_deplib.DATARATE_1344_HZ
while True:
    x, y, z = [value / lis3dh_deplib.STANDARD_GRAVITY for value in lis3dh.acceleration()]
    print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
    time.sleep(0.1)
