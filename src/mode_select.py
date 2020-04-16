#!/usr/bin/python
import rospy
import numpy as np
from mcgreen_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from std_msgs.msg import Int16

multiplier = 1
#movement threshold to prevent accidental input
threshold = 2 
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
        self.up_down = 0
        self.game_data = [1500] * 4
        self.feedback = Int16()
        self.feedback.data = 1
        self.out_upper = Array()
        self.out_upper.arr = [1500] * 2 + [90] * 2
        self.out_lower = Array()
        self.mode_feedback_pub.publish(self.feedback)
    def rec_update(self,data):
        try:
            self.mode = data.ts[1]/500 - 1
            self.reset = int(data.ts[5]/2000)
            self.up_down = data.ts[0]/1000 - 1
        except (ValueError, IndexError):
            print("Waiting for receiver data")
        self.receiver_joystick = list(data.xy)
        self.receiver_joystick = self.receiver_joystick + list(data.ts[3:5])
        self.update()
    def game_update (self, data):
        self.game_data = data.arr
        self.update()
    def update(self):
        upper_data = [1500] * 4
        lower_data = [1500] * 4
        #up_down == 1 -> control drivetrain
        #up_down == 0 -> control head/face
        try:
            if self.mode == 1:
                if self.up_down == 1:
                    lower_data=self.receiver_joystick
                if self.up_down == 0:
                    upper_data=self.receiver_joystick[:-2]
                    #move data from scroll wheels to replace left joystick
                    upper_data[:2] = self.receiver_joystick[-2:]
                    print("input: ", upper_data)
                    #convert values from 1000-2000 range to 0-180 range
                    upper_data[2] = ((float(upper_data[2]) - 1000) / (1000) * (180))
                    upper_data[3] = ((float(upper_data[3]) - 1000) / (1000) * (180))
                    for x in range(2,4):
                        if abs(upper_data[x] - 90) > threshold:
                            # print("current: ",self.out_upper.arr[x])
                            increment = multiplier*np.sign(upper_data[x] - 90)
                            if increment + self.out_upper.arr[x] > 180:
                                upper_data[x]=180
                            elif increment + self.out_upper.arr[x] < 0:
                                upper_data[x]=0
                            else:
                                upper_data[x] = self.out_upper.arr[x] + increment
                        else:
                            upper_data[x] = self.out_upper.arr[x]
                if self.reset == 1:
                    upper_data[2:] = [90,90]
        except IndexError:
            print("Waiting for receiver data")
        if self.mode == 2:
            upper_data = self.game_data
            if self.up_down == 1:
                lower_data = self.receiver_joystick
        if self.mode == 3:
            upper_data = self.game_data
        if self.feedback.data != self.mode:
            self.feedback.data=self.mode
            self.mode_feedback_pub.publish(self.feedback)
        #move forward or backward
        print("final: ", upper_data)
        self.out_upper.arr = upper_data
        self.out_lower.arr = lower_data
        self.upper_safety_pub.publish(self.out_upper)
        self.lower_safety_pub.publish(self.out_lower)


if __name__ == "__main__":
    try:
        rospy.init_node("mode_select")
        mode = Mode_selector()
        rospy.spin()
    except KeyboardInterrupt:
        print("keyboard interrupt")

