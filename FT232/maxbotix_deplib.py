import time
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
from micropython import const

class MAXBOTIX_I2C:
    def __init__(self, ft232h, address=224):
        self.i2c = FT232H.I2CDevice(ft232h, 225 >> 1)
        self.i2c.ping
        self.start_sensor(address)
    
    def start_sensor(self, bit8address):
        errorlevel = 0
        bit8address = bit8address & 0B11111110
        self.i2c.writeRaw8(81)
        
    def read_sensor(self, bit8address):
        bit8address = bit8address | 0B00000001
        range_highbyte = i2c_read(0)
        range_lowbyte = i2c_read(1)
        rangee = (range_highbyte * 256) + range_lowbyte;
        return rangee
