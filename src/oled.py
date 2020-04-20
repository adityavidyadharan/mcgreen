#!/usr/bin/python3
import rospy
# from node_control.msg import Peripheral, Arm, Sensor, Joystick, Array
from std_msgs.msg import Int16, String, Bool
from mcgreen_control.msg import Array
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1327
from PIL import ImageFont, ImageDraw
from time import sleep
import textwrap


serial = spi(device=0, port=0)
device = ssd1327(serial)
font_size = 14
font_name = "FreeMono.ttf"
font = ImageFont.truetype(font_name, font_size)


class Screen:
	MODE_TOPIC = "/mode_feedback"
	GAME_TOPIC = "/current_game"
	UPPER_TOPIC = "/upper_safety"
	EXPRESSION_TOPIC = "/dot_matrix"
	LOWER_TOPIC = "/lower_safety"
	SAFETY_TOPIC = "/safety_feedback"
	def __init__(self):
		self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_set)
		self.game_sub = rospy.Subscriber(self.GAME_TOPIC, String, self.game_set)
		self.upper_sub = rospy.Subscriber(self.UPPER_TOPIC, Array, self.upper_set)
		self.face_sub  = rospy.Subscriber(self.EXPRESSION_TOPIC, Int16, self.face_set)
		self.safety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Bool, self.safety_set)
		self.mode = 1
		self.game = ""
		self.face = "Neutral"
		self.upper=[1500] * 2 + [90] * 2
		self.lower=[1500] * 4
		self.safe = "SAFE"
		self.line = 0
		self.time = 0

	def mode_set(self, data):
		self.mode = data.data

	def safety_set(self, data):
		if data.data == True:
			self.safe = "SAFE"
		else:
			self.safe = "WARNING"

	def upper_set(self, data):
		self.upper = data.arr

	def game_set(self, data):
		self.game = data.data

	def face_set(self, data):
		self.face = data.data
		if self.face == 0:
			self.face = "Warn"
		elif self.face < 4:
			self.face = "Happy " + str(self.face)
		elif self.face >4:
			self.face = "Sad " + str(self.face)
		else:
			self.face = "Neutral"

	def display(self):
		self.line = 0
		# print(self.mode)
		# print(self.game)
		with canvas(device) as draw:
			#draw.rectangle(device.bounding_box, outline="white", fill="black")
		# w, h = draw.textsize(text="Mode: " + str(self.mode), font=font)
		# left = (device.width - w) / 2
		# top = (device.height - h) / 2
			#draw.text((0, self.line*font_size), self.modify_text("Game: " + self.game), font=font, fill="white")
			#draw.text((0, self.line*font_size), self.modify_text("Mode: " + str(self.mode)), font=font, fill="white")
			self.write_text("Mode: " + str(self.mode), draw)
			self.write_text("Game: " + self.game, draw)
			self.write_text("Head Position: ", draw)
			self.write_text(str(self.upper[2:]), draw)
			self.write_text("Face: " + str(self.face), draw)
			self.write_text("", draw)
			self.write_text("Status: ", draw)
			if self.safe == "SAFE":
				self.write_text(self.safe, draw)
			elif self.time >= 5:
				self.write_text(self.safe, draw)
			if self.time == 10:
				self.time = 0
			#self.d(draw)
			#draw.text((0, 45), "Game: RECYCLE DA" + self.game, font=font, fill="white")
		self.time += 1
	def write_text(self, text, draw): # if text is too long it returns the text with \n
		w = font.getsize(text)[0]
		h = font.getsize(text)[1]
		line_height = font.getsize("hg")[1]
		length = len(text)
		current_size = 0		
		begin = 0
		newlines = 0
		modified_text = ""
		if w <= device.width:
			draw.text((0, self.line), text, font=font, fill="white")
			h = font.getsize(text)[1]
			self.line += line_height
			#return 1
		else:
			for i in range(length):
				current_w = font.getsize(text[begin:i+1])[0]
				current_h = font.getsize(text[begin:i+1])[1]
				#end += 1
				# print(text[begin:i+1], current_w)
				if current_w > 128:
					#modified_text += '\n' + text[i]
					draw.text((0, self.line), text[begin:i], font=font, fill="white")
					h = font.getsize(text[begin:i])[1]
					self.line += line_height
					
					begin = i
				#else:
					#modified_text += text[i]
			draw.text((0, self.line), text[begin:length+1], font=font, fill="white")
			h = font.getsize(text[begin:length+1])[1]
			self.line += line_height
			 
		# print(device.width)
		# print(h)
		# print(w)
			
	def d(self, draw):
		draw.text((0, 45), "Game: RECYCLE DA" + self.game, font=font, fill="white")
if __name__ == "__main__":
	rospy.init_node("status_screen")
	screen = Screen()
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		screen.display()
		rate.sleep()
