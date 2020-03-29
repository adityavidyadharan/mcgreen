#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Array

class Peripheral_in:
    GAME_RECEIVE_TOPIC="/game_motor_send"
    ANGLE_TOPIC="/sensor_data/arm_angles"
    MOTOR_SEND_TOPIC="/game_motors"

    tolerance = 10
    def __init__(self):
        #[right arm angle], [left arm angle]
        self.arm_sub = rospy.Subscriber(self.ANGLE_TOPIC, Array, self.angle_callback)
        self.position_sub = rospy.Subscriber(self.GAME_RECEIVE_TOPIC, Array, self.input_callback)
        self.motor_pub = rospy.Publisher(self.MOTOR_SEND_TOPIC, Array, queue_size = 1)
        self.motor_command = Array()
    def angle_callback(self, data):
        self.angles = data
        self.forward()
    def input_callback(self, data):
        self.input = data.arr
        self.forward()
    def forward(self):
        if self.input[0] > (self.angles[0] + self.tolerance):
            motor_command.arr[0]=1000
        elif self.input[0] < (self.angles[0] - self.tolerance):
            motor_command.arr[0]=2000
        else:
            motor_command.arr[0]=1500
        if self.input[1] > (self.angles[1] + self.tolerance):
            motor_command.arr[1]=1000
        elif self.input[1] < (self.angles[1] - self.tolerance):
            motor_command.arr[1]=2000
        else:
            motor_command.arr[1]=1500
        self.motor_pub.publish(motor_command)


if __name__ == "__main__":
    rospy.init_node("relative_controller")
    peripheral = Peripheral_in()
    rospy.spin()