#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Joystick, Face
from std_msgs.msg import Int16
class feedback_manager:
    FACE_TOPIC_IN = "/dot_matrix"
    MODE_TOPIC = "/mode_feedback"
    SAFETY_TOPIC = "/safety_feedback"
    LED_TOPIC = "/LED_control"
    FACE_TOPIC_OUT="/dot_matrix_send"
    def __init__(self):
        self.feedback = Joystick()
        self.face = Face()
        self.face_sub = rospy.Subscriber(self.FACE_TOPIC_IN, Face, self.face_update)
        self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_update)
        self.safety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Int16, self.safety_update)
        self.arduino_pub = rospy.Publisher(self.LED_TOPIC, Joystick, queue_size = 1)
        self.face_pub = rospy.Publisher(self.FACE_TOPIC_OUT, Face, queue_size = 1)
        self.mode = 1
        self.safety = 1
    def face_update(self, data):
        self.face = data
    def mode_update(self,data):
        self.mode = data.data
        self.update()
    def safety_update(self,data):
        self.safety = data.data
        self.update()
    def update(self):
        if self.safety == 0:
            self.face.Expression = 10
            self.RBG=[255,0,0]
        self.feedback.joy = [self.mode, self.safety]



if __name__ == "__main__":
    rospy.init_node("status_control")
    feedback = feedback_manager()
    r = rospy.Rate(10)
    while not rospy.is_shutdown():
        feedback.arduino_pub.publish(feedback.feedback)
        feedback.face_pub.publish(feedback.face)
        r.sleep()
