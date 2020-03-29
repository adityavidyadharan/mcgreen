import time
import math
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.FT232H as FT232H
import monotonic

# Temporarily disable the built-in FTDI serial driver on Mac & Linux platforms.
FT232H.use_FT232H()
 
# Create an FT232H object that grabs the first available FT232H device found.
ft232h = FT232H.FT232H()

ft232h.setup(4, GPIO.IN)   # Make pin D7 a digital input.
ft232h._mpsse_enable
ft232h._mpsse_sync
ft232h.mpsse_set_clock(30000000)

while True:
    for by in ft232h.mpsse_gpio:
        print(by)


"""
while True:
    if (ft232h.input(4) == GPIO.HIGH):
        current_t = monotonic.monotonic()
        while(ft232h.input(4) != GPIO.LOW):
            pass
        print("distance" + str((monotonic.monotonic()-current_t)/0.000147))

"""
"""
while True:
    while ft232h.input(4) == GPIO.LOW:
        #print("low")
        pass
    current_t = monotonic.monotonic()
    while ft232h.input(4) == GPIO.HIGH:
        pass
    print("distance" + str((monotonic.monotonic()-current_t)/0.000147))
"""

"""
while True:
    if ft232h.input(4)==GPIO.LOW:
        print("low")
    if ft232h.input(4)==GPIO.HIGH:
        print("HIGh")
"""
