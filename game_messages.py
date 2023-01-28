import textwrap

import tcod

from visuals.characters import Characters

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

	def add_message(self, message_text, color=tcod.white):
		#split the message if neccesary, among multiple lines
		message = Message("-" + message_text, color)
		new_msg_lines = textwrap.wrap(message.text, self.width)

		for line in new_msg_lines:
			#if log is full, remove first line
			if len(self.messages) == self.height:
				del self.messages[0]


			#add new line as message object
			self.messages.append(Message(line, message.color))
