#!/usr/bin/env python
import time
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
from micropython import const

class MAXBOTIX_I2C():
    def __init__(self, ft232h, address=112):
        self.i2c = FT232H.I2CDevice(ft232h,112)
        #self.i2c.ping()
        """
        while True:
            #print(self.i2c.ping())
            #time.sleep(0.1)
            self.start_sensor()
            time.sleep(0.2)
            self.read_sensor()
         """   
    def start_sensor(self):
        """
        self.i2c._transaction_start()
        self.i2c._i2c_start()
        self.i2c._i2c_write_bytes([self.i2c._address_byte(False), 81])
        self.i2c._transaction_end()
        """
        #self.i2c._i2c_start
        self.i2c.writeRaw8(81)
        #self.i2c.writeList(81, [])

    
        #self.i2c.write8(224, 81 )
       # self.i2c._i2c_write_bytes([self.i2c._address_byte(False), 81])
        #self.i2c._i2c_stop
        #self.i2c.writeRaw8(81)
        """
        self.i2c._idle()
        self.i2c._transaction_start()
        self.i2c._i2c_start()
        self.i2c._i2c_write_bytes([self.i2c._address_byte(False), 81])
        self.i2c._i2c_stop()
        """

    def read_sensor(self):
        """
        self.i2c._idle()
        self.i2c._transaction_start()
        self.i2c._i2c_start()
        self.i2c._i2c_write_bytes([self.i2c._address_byte(False)])
        self.i2c._i2c_stop()
        self.i2c._i2c_idle()
        self.i2c._i2c_start()
        self.i2c._i2c_write_bytes([self.i2c._address_byte(True)])
        range_highbyte = self.i2c._i2c_read_bytes(1)
        print(range_highbyte)
        self.i2c._i2c_stop
        """

        #print(self.i2c.readRaw8())
        #print(self.i2c.readRaw8())
        #x = self.i2c.readList(225, 2)
        #print(self.i2c.readU8(225))
        #print(self.i2c.readU8(36))
        val = self.i2c.readU16(225)
        #print(self.i2c.readU8(225))
        #print(self.i2c.readU8(225))

        #print(hex(val))
        print(val >> 8), "cm"
        return val >> 8
        #print(self.i2c.readRaw8())
        #print(val)
        #print (val >> 8) & 0xFF | (val & 0xFf), 'cm'
        #print (val >> 8) & 0xFF
