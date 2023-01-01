import tcod

import textwrap

class Message:
	def __init__(self, text, color=tcod.white):
		self.text = text
		self.color = color

class MessageLog:
	def __init__(self, x, y, width, height):
		self.messages = []
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def add_message(self, message):
		#split the message if neccesary, among multiple lines
		new_msg_lines = textwrap.wrap(message.text, self.width)

		for line in new_msg_lines:
			#if log is full, remove first line
			if len(self.messages) == self.height:
				del self.messages[0]


			#add new line as message object
			self.messages.append(Message(line, message.color))
