#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from std_msgs.msg import Int16

class Manager:
    RECEIVER_OUTPUT_TOPIC =  "/receiver_output"
    LEFT_TOPIC = "left_arm_send"
    RIGHT_TOPIC = "right_arm_send" 
    RECEIVER_TOPIC = "/receiver"
    TOGGLE_TOPIC = "/toggle_switches" #deleted
    MOTOR_TOPIC = "/receiver_motors" #deleted
    SENSOR_TOPIC = "/sensor_data" 

    initial_ultra=50
    def __init__(self):
        self.rec_sub = rospy.Subscriber(self.RECEIVER_OUTPUT_TOPIC, Array, self.receiver_callback)
        self.left_sub = rospy.Subscriber(self.LEFT_TOPIC, Arm, self.right_arm_callback)
        self.right_sub = rospy.Subscriber(self.RIGHT_TOPIC, Arm, self.left_arm_callback)
        self.rec_pub = rospy.Publisher(self.RECEIVER_TOPIC, Peripheral, queue_size = 1)
        self.sensor_pub = rospy.Publisher(self.SENSOR_TOPIC, Sensor, queue_size = 1)
        #Intiate variables
        self.sensors = Sensor()
        self.out_receiver = Peripheral()
        #Arm initial values
        self.left_data=Arm()
        self.left_data.ultra=[self.initial_ultra]*2
        self.right_data=Arm()
        self.right_data.ultra=[self.initial_ultra]*2
        self.sensors.ultrasonic=[self.initial_ultra]*4
    def right_arm_callback(self, data):
        self.left_data = data
        self.data_process()
        #convert x,y,z to value | store in right_measure
    def left_arm_callback(self, data):
        self.right_data = data
        self.data_process()
        #convert x,y,z to value | store in left_measure
    def receiver_callback(self, data):
        self.receiver_data = data.arr
        self.receiver_splice()
    def receiver_splice(self):
        self.out_receiver.ts = self.receiver_data[4:]
        self.out_receiver.xy = self.receiver_data[3:1:-1] + self.receiver_data[:2]
        if self.receiver_data[2] == 1518:
            self.out_receiver.xy=[self.out_receiver.xy[0], 1500, self.out_receiver.xy[2], self.out_receiver.xy[3]]
        self.data_publish()
    def data_process(self):
        #sensors.ultrasonic = [right_top, right_bottom, left_top, left_bottom]
        self.sensors.ultrasonic = self.right_data.ultra + self.left_data.ultra
        #sensors.arm_angles=[right_arm, left_arm]
        self.sensors.arm_angles=[10,10]
    def data_publish(self):
        self.sensor_pub.publish(self.sensors)
        self.rec_pub.publish(self.out_receiver)


if __name__ == "__main__":
    rospy.init_node("peripheral_manager")
    peripheral = Manager()
    rospy.spin()