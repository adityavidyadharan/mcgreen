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
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)
counter=0
ch = [1500 for i in range(10)]

def bytes_to_int(bytes):
	result=0
	for b in bytes:
		result = result*256+int(b)
	return result

def talker():
	pub = rospy.Publisher('peripheral_send', Peripheral, queue_size=0)
	rospy.init_node('pi', anonymous=True)
	rate=rospy.Rate(20)
	
#while 1:
	while not rospy.is_shutdown():
	
		a = ser.read(1)
		x = hexlify(a)
		#print(x)
		if x == "20":
			a = ser.read(1)
			x = hexlify(a)
			if x == "40":
				for i in range(10):
					b = ser.read(1)
					a = ser.read(1)
					#print(long(hexlify(a+b),16)),
					#print(int.from_bytes(a+b)),
					global ch
					if hexlify(a+b) != "":
						ch[i] = int(hexlify(a+b),16)
					else:
						ch = [0,0,0,0,0,0,0,0,0,0]

					#ch[i] = int(6)
					#print(ord(a+b))
					
				#print(ch)
				#print("\n")
		elif x == "":
			ch = [0,0,0,0,0,0,0,0,0,0]

		#rate.sleep()
		msg = Peripheral()
		
		msg.ch = ch
		pub.publish(msg)

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

