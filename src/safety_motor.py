#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from std_msgs.msg import Int16
class safety_break:
    TOGGLE_TOPIC="/receiver"
    UPPER_IN = "/upper_motors"
    LOWER_IN = "/lower_motors"
    US_TOPIC = "/sensor_data"
    UPPER_OUT = "/upper_safety"
    LOWER_OUT = "/lower_safety"
    FEEDBACK_TOPIC = "/safety_feedback"
    threshold = 10
    def __init__(self):
        self.upper_safe = Array()
        self.lower_safe = Array()
        self.feedback = Int16()
        self.feedback.data = 1
        self.safe = 1
        self.upper = [1500]*2
        self.lower = [1500]*2
        self.up_sub = rospy.Subscriber(self.UPPER_IN, Array, self.up_update)
        self.low_sub = rospy.Subscriber(self.LOWER_IN, Array, self.low_update)
        self.sensor_sub = rospy.Subscriber(self.US_TOPIC, Sensor, self.sensor_update)
        self.tog_sub = rospy.Subscriber(self.TOGGLE_TOPIC, Peripheral, self.toggle_update)
        self.upper_pub = rospy.Publisher(self.UPPER_OUT, Array, queue_size = 1)
        self.lower_pub = rospy.Publisher(self.LOWER_OUT, Array, queue_size = 1)
        self.safety_feedback_pub = rospy.Publisher(self.FEEDBACK_TOPIC, Int16, queue_size = 1)
        self.safety_feedback_pub.publish(self.feedback)
        self.us=[50]*4
    def up_update(self,data):
        self.upper = data.arr
        self.update()
    def low_update(self,data):
        self.lower = data.arr
        self.update()
    def sensor_update(self, data):
        #Replace 0's with old value
        for old, new in zip(self.us, enumerate(data.ultrasonic)):
            if new[1] == 0:
                #data.ultrasonic[b[0]]=2000
                data.ultrasonic[b[0]]=old
        self.us = data.ultrasonic
        self.update()
    def toggle_update(self, data):
        self.safety_clear = data.ts[5]
        self.update()
    def update(self):
        if all(item < self.threshold for item in self.us):
            self.upper_safe.arr = [1500]*4
            self.lower_safe.arr = [1500]*4
            self.safe = 0
        if self.safe == 0 and self.safety_clear == 2000:
            self.safe = 1
        if self.safe == 1:
            self.upper_safe.arr = self.upper
            self.lower_safe.arr = self.lower
        if self.safe != self.feedback.data:
            self.feedback.data = self.safe
            self.safety_feedback_pub.publish(self.feedback)
        #self.upper_pub.publish(self.upper_safe)
        #self.lower_pub.publish(self.lower_safe)


if __name__ == "__main__":
    rospy.init_node("safety_cutoff")
    safe = safety_break()
    r = rospy.Rate(50)
    while not rospy.is_shutdown():
        safe.upper_pub.publish(safe.upper_safe)
        safe.lower_pub.publish(safe.lower_safe)
        r.sleep()
