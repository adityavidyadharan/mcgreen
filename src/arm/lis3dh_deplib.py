#!/usr/bin/env python
import time
import math
from collections import namedtuple
import struct
import Adafruit_GPIO.FT232H as FT232H
import Adafruit_GPIO as GPIO
from micropython import const


# Register addresses:
# pylint: disable=bad-whitespace
_REG_OUTADC1_L   = const(0x08)
_REG_WHOAMI      = const(0x0F)
_REG_TEMPCFG     = const(0x1F)
_REG_CTRL1       = const(0x20)
_REG_CTRL3       = const(0x22)
_REG_CTRL4       = const(0x23)
_REG_CTRL5       = const(0x24)
_REG_OUT_X_L     = const(0x28)
_REG_INT1SRC     = const(0x31)
_REG_CLICKCFG    = const(0x38)
_REG_CLICKSRC    = const(0x39)
_REG_CLICKTHS    = const(0x3A)
_REG_TIMELIMIT   = const(0x3B)
_REG_TIMELATENCY = const(0x3C)
_REG_TIMEWINDOW  = const(0x3D)

# Register value constants:
RANGE_16_G               = const(0b11)    # +/- 16g
RANGE_8_G                = const(0b10)    # +/- 8g
RANGE_4_G                = const(0b01)    # +/- 4g
RANGE_2_G                = const(0b00)    # +/- 2g (default value)
DATARATE_1344_HZ         = const(0b1001)  # 1.344 KHz
DATARATE_400_HZ          = const(0b0111)  # 400Hz
DATARATE_200_HZ          = const(0b0110)  # 200Hz
DATARATE_100_HZ          = const(0b0101)  # 100Hz
DATARATE_50_HZ           = const(0b0100)  # 50Hz
DATARATE_25_HZ           = const(0b0011)  # 25Hz
DATARATE_10_HZ           = const(0b0010)  # 10 Hz
DATARATE_1_HZ            = const(0b0001)  # 1 Hz
DATARATE_POWERDOWN       = const(0)
DATARATE_LOWPOWER_1K6HZ  = const(0b1000)
DATARATE_LOWPOWER_5KHZ   = const(0b1001)

# Other constants
STANDARD_GRAVITY = 9.806
# pylint: enable=bad-whitespace

# the named tuple returned by the class
AccelerationTuple = namedtuple("acceleration", ("x", "y", "z"))

class LIS3DH_I2C:
    def __init__(self, ft232h, address=0x18):
        self.i2c = FT232H.I2CDevice(ft232h, address)
        self.buffer = bytearray(6)
         # Reboot
        self.i2c.write8(_REG_CTRL5, 0x80)
        time.sleep(0.01)  # takes 5ms
        # Enable all axes, normal mode.
        self.i2c.write8(_REG_CTRL1, 0x07)
        # Set 400Hz data rate.
        self.data_rate = DATARATE_400_HZ
        # High res & BDU enabled.
        self.i2c.write8(_REG_CTRL4, 0x88)
        # Enable ADCs.
        self.i2c.write8(_REG_TEMPCFG, 0x80)
        # Latch interrupt for INT1
        self.i2c.write8(_REG_CTRL5, 0x08)
        
        self.i2c.write8(0,0)
        self.i2c.write8(1,0)
        self.i2c.write8(2,0)
        self.i2c.write8(3,0)
        self.i2c.write8(4,0)
        self.i2c.write8(5,0)
        self.i2c.write8(6,0)
        self.i2c.write8(7,255)
        self.i2c.write8(8,0)
        self.i2c.write8(9,125)
        self.i2c.write8(10,128)
        self.i2c.write8(11,32)
        self.i2c.write8(12,0)
        self.i2c.write8(13,192)
        self.i2c.write8(14,0)
        self.i2c.write8(15,51)
        self.i2c.write8(16,26)
        self.i2c.write8(17,78)
        self.i2c.write8(18,52)
        self.i2c.write8(19,33)
        self.i2c.write8(20,162)
        self.i2c.write8(21,32)
        self.i2c.write8(22,36)
        self.i2c.write8(23,33)
        self.i2c.write8(24,34)
        self.i2c.write8(25,161)
        self.i2c.write8(26,128)
        self.i2c.write8(27,132)
        self.i2c.write8(28,192)
        self.i2c.write8(29,0)
        self.i2c.write8(30,16)
        self.i2c.write8(31,128)
        self.i2c.write8(32,119)
        self.i2c.write8(33,0)
        self.i2c.write8(34,0)
        self.i2c.write8(35,136)
        self.i2c.write8(36,8)
        self.i2c.write8(37,0)
        self.i2c.write8(38,0)
        self.i2c.write8(39,255)
        self.i2c.write8(40,128)
        self.i2c.write8(41,254)
        self.i2c.write8(42,32)
        self.i2c.write8(43,1)
        self.i2c.write8(44,208)
        self.i2c.write8(45,60)
        self.i2c.write8(46,0)
        self.i2c.write8(47,32)
        self.i2c.write8(48,0)
        self.i2c.write8(49,0)
        self.i2c.write8(50,0)
        self.i2c.write8(51,0)
        self.i2c.write8(52,0)
        self.i2c.write8(53,0)
        self.i2c.write8(54,0)
        self.i2c.write8(55,0)
        self.i2c.write8(56,0)
        self.i2c.write8(57,0)
        self.i2c.write8(58,0)
        self.i2c.write8(59,0)
        self.i2c.write8(60,0)
        self.i2c.write8(61,0)
        self.i2c.write8(62,0)
        self.i2c.write8(63,0)
        self.i2c.write8(64,0)
        self.i2c.write8(65,0)
        self.i2c.write8(66,0)
        self.i2c.write8(67,0)
        self.i2c.write8(68,0)
        self.i2c.write8(69,0)
        self.i2c.write8(70,0)
        self.i2c.write8(71,0)
        self.i2c.write8(72,0)
        self.i2c.write8(73,0)
        self.i2c.write8(74,0)
        self.i2c.write8(75,0)
        self.i2c.write8(76,0)
        self.i2c.write8(77,0)
        self.i2c.write8(78,0)
        self.i2c.write8(79,0)
        self.i2c.write8(80,0)
        self.i2c.write8(81,0)
        self.i2c.write8(82,0)
        self.i2c.write8(83,0)
        self.i2c.write8(84,0)
        self.i2c.write8(85,0)
        self.i2c.write8(86,0)
        self.i2c.write8(87,0)
        self.i2c.write8(88,0)
        self.i2c.write8(89,0)
        self.i2c.write8(90,0)
        self.i2c.write8(91,0)
        self.i2c.write8(92,0)
        self.i2c.write8(93,0)
        self.i2c.write8(94,0)
        self.i2c.write8(95,0)
        self.i2c.write8(96,0)
        self.i2c.write8(97,0)
        self.i2c.write8(98,0)
        self.i2c.write8(99,0)
        self.i2c.write8(100,0)
        self.i2c.write8(101,0)
        self.i2c.write8(102,0)
        self.i2c.write8(103,0)
        self.i2c.write8(104,0)
        self.i2c.write8(105,0)
        self.i2c.write8(106,0)
        self.i2c.write8(107,0)
        self.i2c.write8(108,0)
        self.i2c.write8(109,0)
        self.i2c.write8(110,0)
        self.i2c.write8(111,0)
        self.i2c.write8(112,0)
        self.i2c.write8(113,0)
        self.i2c.write8(114,0)
        self.i2c.write8(115,0)
        self.i2c.write8(116,0)
        self.i2c.write8(117,0)
        self.i2c.write8(118,0)
        self.i2c.write8(119,0)
        self.i2c.write8(120,0)
        self.i2c.write8(121,0)
        self.i2c.write8(122,0)
        self.i2c.write8(123,0)
        self.i2c.write8(124,0)
        self.i2c.write8(125,0)
        self.i2c.write8(126,0)
        self.i2c.write8(127,0)
        self.i2c.write8(128,0)
        self.i2c.write8(129,0)
        self.i2c.write8(130,0)
        self.i2c.write8(131,0)
        self.i2c.write8(132,0)
        self.i2c.write8(133,0)
        self.i2c.write8(134,0)
        self.i2c.write8(135,255)
        self.i2c.write8(136,0)
        self.i2c.write8(137,249)
        self.i2c.write8(138,64)
        self.i2c.write8(139,186)
        self.i2c.write8(140,128)
        self.i2c.write8(141,39)
        self.i2c.write8(142,0)
        self.i2c.write8(143,51)
        self.i2c.write8(144,26)
        self.i2c.write8(145,78)
        self.i2c.write8(146,52)
        self.i2c.write8(147,33)
        self.i2c.write8(148,162)
        self.i2c.write8(149,32)
        self.i2c.write8(150,36)
        self.i2c.write8(151,33)
        self.i2c.write8(152,34)
        self.i2c.write8(153,161)
        self.i2c.write8(154,128)
        self.i2c.write8(155,132)
        self.i2c.write8(156,192)
        self.i2c.write8(157,0)
        self.i2c.write8(158,16)
        self.i2c.write8(159,128)
        self.i2c.write8(160,119)
        self.i2c.write8(161,0)
        self.i2c.write8(162,0)
        self.i2c.write8(163,136)
        self.i2c.write8(164,8)
        self.i2c.write8(165,0)
        self.i2c.write8(166,0)
        self.i2c.write8(167,255)
        self.i2c.write8(168,128)
        self.i2c.write8(169,254)
        self.i2c.write8(170,0)
        self.i2c.write8(171,1)
        self.i2c.write8(172,176)
        self.i2c.write8(173,60)
        self.i2c.write8(174,0)
        self.i2c.write8(175,32)
        self.i2c.write8(176,0)
        self.i2c.write8(177,0)
        self.i2c.write8(178,0)
        self.i2c.write8(179,0)
        self.i2c.write8(180,0)
        self.i2c.write8(181,0)
        self.i2c.write8(182,0)
        self.i2c.write8(183,0)
        self.i2c.write8(184,0)
        self.i2c.write8(185,0)
        self.i2c.write8(186,0)
        self.i2c.write8(187,0)
        self.i2c.write8(188,0)
        self.i2c.write8(189,0)
        self.i2c.write8(190,0)
        self.i2c.write8(191,0)
        self.i2c.write8(192,0)
        self.i2c.write8(193,0)
        self.i2c.write8(194,0)
        self.i2c.write8(195,0)
        self.i2c.write8(196,0)
        self.i2c.write8(197,0)
        self.i2c.write8(198,0)
        self.i2c.write8(199,0)
        self.i2c.write8(200,0)
        self.i2c.write8(201,0)
        self.i2c.write8(202,0)
        self.i2c.write8(203,0)
        self.i2c.write8(204,0)
        self.i2c.write8(205,0)
        self.i2c.write8(206,0)
        self.i2c.write8(207,0)
        self.i2c.write8(208,0)
        self.i2c.write8(209,0)
        self.i2c.write8(210,0)
        self.i2c.write8(211,0)
        self.i2c.write8(212,0)
        self.i2c.write8(213,0)
        self.i2c.write8(214,0)
        self.i2c.write8(215,0)
        self.i2c.write8(216,0)
        self.i2c.write8(217,0)
        self.i2c.write8(218,0)
        self.i2c.write8(219,0)
        self.i2c.write8(220,0)
        self.i2c.write8(221,0)
        self.i2c.write8(222,0)
        self.i2c.write8(223,0)
        self.i2c.write8(224,0)
        self.i2c.write8(225,0)
        self.i2c.write8(226,0)
        self.i2c.write8(227,0)
        self.i2c.write8(228,0)
        self.i2c.write8(229,0)
        self.i2c.write8(230,0)
        self.i2c.write8(231,0)
        self.i2c.write8(232,0)
        self.i2c.write8(233,0)
        self.i2c.write8(234,0)
        self.i2c.write8(235,0)
        self.i2c.write8(236,0)
        self.i2c.write8(237,0)
        self.i2c.write8(238,0)
        self.i2c.write8(239,0)
        self.i2c.write8(240,0)
        self.i2c.write8(241,0)
        self.i2c.write8(242,0)
        self.i2c.write8(243,0)
        self.i2c.write8(244,0)
        self.i2c.write8(245,0)
        self.i2c.write8(246,0)
        self.i2c.write8(247,0)
        self.i2c.write8(248,0)
        self.i2c.write8(249,0)
        self.i2c.write8(250,0)
        self.i2c.write8(251,0)
        self.i2c.write8(252,0)
        self.i2c.write8(253,0)
        self.i2c.write8(254,0)
        self.i2c.write8(255,0)

        device_id = self._read_register_byte(_REG_WHOAMI)
        if device_id != 0x33:
            raise RuntimeError("Failed to find LIS3DH!")
    

    def data_rate(self):
        ctl1 = self._read_register_byte(_REG_CTRL1)
        return (ctl1 >> 4) & 0x0F

    def data_rate(self, rate):
        ctl1 = self._read_register_byte(_REG_CTRL1)
        ctl1 &= ~(0xF0)
        ctl1 |= rate << 4
        self._write_register_byte(_REG_CTRL1, ctl1)

    def range(self):
        ctl4 = self._read_register_byte(_REG_CTRL4)
        return (ctl4 >> 4) & 0x03
    
    def range(self, range_value):
        ctl4 = self._read_register_byte(_REG_CTRL4)
        ctl4 &= ~0x30
        ctl4 |= range_value << 4
        self._write_register_byte(_REG_CTRL4, ctl4)


    def _read_register(self,register, length):
        for i in range(length):
            self.buffer[i] = self.i2c.readU8(register+i)
        return self.buffer
    
    def _read_register_byte(self,register):
        return self._read_register(register,1)[0]

    def _write_register_byte(register, value):
        self.i2c.write8(register, value)

    def acceleration(self):
        """The x, y, z acceleration values returned in a 3-tuple and are in m / s ^ 2."""
        divider = 1
        accel_range = self.range
        if accel_range == RANGE_16_G:
            divider = 1365
        elif accel_range == RANGE_8_G:
            divider = 4096
        elif accel_range == RANGE_4_G:
            divider = 8190
        elif accel_range == RANGE_2_G:
            divider = 16380

        x, y, z = struct.unpack('<hhh', self._read_register(_REG_OUT_X_L | 0x80, 6))
        
        x = (x / float(divider)) * STANDARD_GRAVITY
        y = (y / float(divider)) * STANDARD_GRAVITY
        z = (z / float(divider)) * STANDARD_GRAVITY
        
        return (x,y,z)
