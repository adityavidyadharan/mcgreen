#!/usr/bin/env python
import time
import serial
import chardet
import rospy
from mcgreen_control.msg import Peripheral, Arm, Sensor, Joystick
from binascii import hexlify
from binascii import unhexlify
from threading import Timer

class Receiver:
	def __init__ (self):
		self.pub = rospy.Publisher('peripheral_send', Peripheral, queue_size=5)
		self.ser = serial.Serial(
			port='/dev/ttyUSB0',
			baudrate=115200,
			#parity=serial.PARITY_NONE,
			#stopbits=serial.STOPBITS_ONE,
			#bytesize=serial.EIGHTBITS,
			timeout=1
		)
		self.ch = [0,0,0,0,0,0,0,0,0,0]
	def process(self):
		a = ser.read(1)
		x = hexlify(a)

		if x == "20":
			a = ser.read(1)
			x = hexlify(a)
			if x == "40":
				#print(ser.in_waiting)
				a = ser.read(20)
				#print(hexlify(a))
				for i in range(10):
					self.ch[i]=int(hexlify(a[i*2+1]+a[i*2]),16)
				#rate.sleep()
				msg = Peripheral()

				msg.ch = self.ch
				self.pub.publish(msg)

		elif x == "":
			msg = Peripheral()

			msg.ch = self.ch
			self.pub.publish(msg)

if __name__ == "__main__":
    rospy.init_node("serial_receive_class")
    mode = Receiver()
    rospy.spin()
