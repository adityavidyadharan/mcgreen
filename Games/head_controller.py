#!/usr/bin/python

import rospy
import rosnode
from std_msgs.msg import Int16, String
from mcgreen_control.msg import Array

# 1-3 -> Happy Faces
# 4   -> Neutral
# 5-6 -> Sad Faces
class Head_comm:
    FACE_EXPRESSION = "/facial_expression"
    HEAD_TOPIC = "/game_motors"
    GAME_TOPIC = "/current_game"
    def __init__ (self, game):
        rospy.init_node("Head_Controller")
        rospy.on_shutdown(self.game_cleanup)
        self.face_pub=rospy.Publisher(self.FACE_EXPRESSION, Int16, queue_size=1)
        self.head_pub=rospy.Publisher(self.HEAD_TOPIC, Array, queue_size=1)
        self.game_pub=rospy.Publisher(self.GAME_TOPIC, String, queue_size=1)
        self.expression=Int16()
        self.expression.data=4
        self.head=Array()
        self.head.arr=[1500,1500,90,90]
        self.name=String()
        self.name.data = game
        self.game_pub.publish(self.name)
    def face_update(self, face):
        self.expression.data=face
        self.face_pub.publish(self.expression)
        self.game_pub.publish(self.name)
    def head_update(self, angle):
        self.head.arr[2:]=angle
        self.head_pub.publish(self.head)
    def game_cleanup(self):
        self.name.data = ""
        self.game_pub.publish(self.name)

if __name__=="__main__":
    try:
        rospy.init_node("Head_Controller")
        face_controller = Head_comm("init")
        rospy.spin()
    except KeyboardInterrupt:
        pass
