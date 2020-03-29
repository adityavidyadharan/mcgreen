#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from std_msgs.msg import Int16

class Mode_selector:
    RECEIVER_TOPIC = "/receiver"
    UPPER_TOPIC = "/upper_motors"
    LOWER_TOPIC = "/lower_motors"
    GAME_TOPIC = "/game_motors"
    FEEDBACK_TOPIC = "/mode_feedback"
    def __init__(self):
        self.rec_sub = rospy.Subscriber(self.RECEIVER_TOPIC, Peripheral, self.rec_update)
        self.game_sub = rospy.Subscriber(self.GAME_TOPIC, Array, self.game_update)
        self.upper_safety_pub = rospy.Publisher(self.UPPER_TOPIC, Array, queue_size = 1)
        self.lower_safety_pub = rospy.Publisher(self.LOWER_TOPIC, Array, queue_size = 1)
        self.mode_feedback_pub = rospy.Publisher(self.FEEDBACK_TOPIC, Int16, queue_size = 1)
        self.mode = 1
        self.up_low = 0
        self.arduino_data=[1500,1500,1500,1500]
        self.game_data=[1500,1500, 1500, 1500]
        self.feedback = Int16()
        self.feedback.data = 1
        self.mode_feedback_pub.publish(self.feedback)
    def rec_update(self,data):
        self.mode = data.ts[1]/500 - 1
        self.up_low = data.ts[0]/1000 - 1
        self.receiver_joystick = data.xy
        self.update()
    def game_update (self, data):
        self.game_data = data.arr
        self.update()
    def update(self):
        self.out_upper = Array()
        self.out_lower = Array()
        #up_low == 1 -> control drivetrain
        #up_low == 0 -> control head/shoulders
        if self.mode == 1:
            self.out_lower.arr = [1500]*4
            self.out_upper.arr =[1500]*4
            if self.up_low == 1:
                self.out_lower.arr=self.receiver_joystick
            if self.up_low == 0:
                self.out_upper.arr=self.receiver_joystick
        if self.mode == 2:
            self.out_upper.arr = self.game_data
            self.out_lower.arr= [1500]*4
            if self.up_low == 1:
                self.out_lower.arr = self.receiver_joystick

        if self.mode == 3:
            self.out_upper.arr = self.game_data
            self.out_lower.arr = [1500]*4
        
        if self.feedback.data != self.mode:
            self.feedback.data=self.mode
            self.mode_feedback_pub.publish(self.feedback)


        self.upper_safety_pub.publish(self.out_upper)
        self.lower_safety_pub.publish(self.out_lower)


if __name__ == "__main__":
    try:
        rospy.init_node("mode_select")
        mode = Mode_selector()
        rospy.spin()
    except KeyboardInterrupt:
        print("keyboard interrupt")
