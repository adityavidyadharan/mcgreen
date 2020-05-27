#!/usr/bin/python
import rospy
from mcgreen_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from numpy import interp
from std_msgs.msg import Int16, Bool



class safety_break:
    TOGGLE_TOPIC="/receiver"
    UPPER_IN = "/upper_motors"
    LOWER_IN = "/lower_motors"
    US_TOPIC = "/sensor_data"
    UPPER_OUT = "/upper_safety"
    LOWER_OUT = "/lower_safety"
    FEEDBACK_TOPIC = "/safety_feedback"
    FACE_IN="/facial_expression"
    FACE_OUT="/dot_matrix"
    threshold = rospy.get_param("peripheral/threshold_ultra")
    def __init__(self):
        self.upper_safe = Array()
        self.lower_safe = Array()
        self.feedback = Bool()
        self.feedback.data = True
        self.safe = True
        self.safety_clear = 1000
        self.upper = [1500]*2 + [90] * 2
        self.lower = [1500]*4
        self.face = Int16()
        self.face.data = 4
        self.up_sub = rospy.Subscriber(self.UPPER_IN, Array, self.up_update)
        self.low_sub = rospy.Subscriber(self.LOWER_IN, Array, self.low_update)
        self.sensor_sub = rospy.Subscriber(self.US_TOPIC, Sensor, self.sensor_update)
        self.tog_sub = rospy.Subscriber(self.TOGGLE_TOPIC, Peripheral, self.toggle_update)
        self.face_sub = rospy.Subscriber(self.FACE_IN, Int16, self.face_update)
        self.face_pub = rospy.Publisher(self.FACE_OUT, Int16, queue_size=1)
        self.upper_pub = rospy.Publisher(self.UPPER_OUT, Array, queue_size = 1)
        self.lower_pub = rospy.Publisher(self.LOWER_OUT, Array, queue_size = 1)
        self.safety_feedback_pub = rospy.Publisher(self.FEEDBACK_TOPIC, Bool, queue_size = 1)
        self.safety_feedback_pub.publish(self.feedback)
        self.us=[50]*4
    def up_update(self,data):
        self.upper = list(data.arr)
    def low_update(self,data):
        self.lower = list(data.arr)
    def face_update(self,data):
        self.face = data
    def sensor_update(self, data):
        #Replace 0's with old value
        for old, new in zip(self.us, enumerate(data.ultrasonic)):
            if new[1] == 0:
                #data.ultrasonic[b[0]]=2000
                data.ultrasonic[b[0]]=old
        self.us = data.ultrasonic
    def toggle_update(self, data):
        try:
            self.safety_clear = data.ts[5]
        except IndexError:
            self.safety_clear = 1000
    def update(self):
        # upper_safe = [arm_left, arm_right, head_x, head_y]
        if not all(item > self.threshold for item in self.us):
            self.lower_safe.arr = [1500]*4
            self.upper_safe.arr[:2] = [1500]*2
            self.safe = False
        if self.safe == False:
            warn_face = Int16()
            warn_face.data = 0
            self.face_pub.publish(warn_face)
            if self.safety_clear == 2000:
                self.safe = True
        if self.safe == True:
            self.lower_safe.arr = self.lower
            self.upper_safe.arr = self.upper
            self.face_pub.publish(self.face)
        if self.safe != self.feedback.data:
            self.feedback.data = self.safe
            self.safety_feedback_pub.publish(self.feedback)
        self.upper_safe.arr[2:] = self.upper[2:]
        self.upper_pub.publish(self.upper_safe)
        self.lower_pub.publish(self.lower_safe)


if __name__ == "__main__":
    rospy.init_node("safety_cutoff")
    safe = safety_break()
    #rospy.spin()
    r = rospy.Rate(50)
    while not rospy.is_shutdown():
        safe.update()
        r.sleep()
