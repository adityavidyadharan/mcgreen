import time
import math
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
import maxbotix_deplib


FT232H.use_FT232H()
ft232h = FT232H.FT232H(serial='black')
address = 224
#i2c = FT232H.I2CDevice(ft232h, address)
maxbotix = maxbotix_deplib.MAXBOTIX_I2C(ft232h, address)









