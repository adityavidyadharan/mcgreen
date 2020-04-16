#!/usr/bin/env python
import time
import serial
import chardet
import rospy
from mcgreen_control.msg import Peripheral, Arm, Sensor, Joystick
from binascii import hexlify
from binascii import unhexlify 
from threading import Timer
ser = serial.Serial(
	port='/dev/ttyUSB0',
	baudrate=115200,
	#parity=serial.PARITY_NONE,
	#stopbits=serial.STOPBITS_ONE,
	#bytesize=serial.EIGHTBITS,
	timeout=1
)
counter=0
ch = [0,0,0,0,0,0,0,0,0,0]

def bytes_to_int(bytes):
	result=0
	for b in bytes:
		result = result*256+int(b)
	return result

def talker():
	pub = rospy.Publisher('receiver_send', Peripheral, queue_size=10)
	rospy.init_node('pi', anonymous=True)
	rate=rospy.Rate(400)
	
#while 1:
	global ch
	#ch = [0,0,0,0,0,0,0,0,0,0]
	while not rospy.is_shutdown():
		
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
					ch[i]=int(hexlify(a[i*2+1]+a[i*2]),16)
				rate.sleep()
			        msg = Peripheral()
		
				msg.ch = ch
				pub.publish(msg)

		elif x == "":
			ch = [0,0,0,0,0,0,0,0,0,0]
			msg = Peripheral()
		
			msg.ch = ch
			pub.publish(msg)


		
		


if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

