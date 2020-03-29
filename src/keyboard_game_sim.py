#!/usr/bin/python
import rospy
from node_control.msg import Peripheral, Arm, Sensor, Joystick

class Game_out:
    OUTPUT_TOPIC = "/game_motors"
    def __init__(self):
        self.game_pub = rospy.Publisher(self.OUTPUT_TOPIC, Joystick, queue_size = 1)
        self.data = Joystick()
        self.data.joy = [1500,1500, 1500, 1500]
        self.data.game = "Simulated"
    def prompt(self):
        print("Left joystick values: ")
        self.data.joy[0] = int(input("simulated x: "))
        self.data.joy[1] = int(input("simulated y: "))
        print("Rigtt joystick values: ")
        self.data.joy[2] = int(input("simulated x: "))
        self.data.joy[3] = int(input("simulated y: "))

        self.game_pub.publish(self.data)


if __name__ == "__main__":
    rospy.init_node("game_data_sim")
    game = Game_out()
    while not rospy.is_shutdown():
        game.prompt()
