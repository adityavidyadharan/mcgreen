#!/usr/bin/env python
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

#vertical controller attached to GPIO 12
#horizontal controller attached to GPIO 13

class servo_controller:
    SERVO_TOPIC = "/upper_safety"
    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.SERVO_TOPIC, Array, self.servo_callback)
        GPIO.setwarnings(False)			#disable warnings
        GPIO.setmode(GPIO.BOARD)		#set pin numbering system
        GPIO.setup(11,GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        self.vertical_controller = GPIO.PWM(11,50)		#create PWM instance with frequency
        self.horizontal_controller = GPIO.PWM(13, 50)
        self.vertical_controller.start(50)				#start PWM of required Duty Cycle
        self.horizontal_controller.start(50)
	for x in range(0,90):
		self.vertical_controller.ChangeDutyCycle(2+float(x*2)/18)
		#time.sleep(0.1)
		#self.vertical_controller.ChangeDutyCycle(0)
    def servo_callback(self, data):
        print("raw: " + str(data.arr))
	horizontal_angle = 2 + float(data.arr[2])/18
        vertical_angle=2+float(data.arr[3])/18
	self.vertical_controller.ChangeDutyCycle(vertical_angle)
        self.horizontal_controller.ChangeDutyCycle(horizontal_angle)
	#time.sleep(0.5)
	#self.vertical_controller.ChangeDutyCycle(0)
	#self.horizontal_controller.ChangeDutyCycle(0)
	print(vertical_angle, horizontal_angle)        

    def clean(self):
        self.vertical_controller.ChangeDutyCycle(7)
        self.horizontal_controller.ChangeDutyCycle(7)
        print("base position")

if __name__ == "__main__":
    try:
        rospy.init_node("head_controller")
        controller = servo_controller()
        rospy.spin()
        rospy.on_shutdown(controller.clean)
    except KeyboardInterrupt:
        print("keyboard interrupt")

