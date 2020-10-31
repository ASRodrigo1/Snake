import cv2
import numpy as np
import random

x, y, vel = 15, 15, (15, 0)
startx, starty = 0, 0
screenx, screeny = 512, 512

def create_image():

	cv2.rectangle(img, (food[0], food[1]), (food[0] + 10, food[1] + 10), (0, 255, 255), -1) # Yellow food
	count = 0
	for part in snake.body_parts:

		count += 1

		part.pos1[0] += part.vel[0]
		part.pos1[1] += part.vel[1]
		part.pos2[0] += part.vel[0]
		part.pos2[1] += part.vel[1]

		pos1, pos2 = part.pos1, part.pos2
		cv2.rectangle(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 255, 0), -1)

		### Player outside window
		if (part.pos1[0] > screenx) or (part.pos2[0] > screenx) or (part.pos1[0] < 0) or (part.pos2[0] < 0) or \
		   (part.pos1[1] > screeny) or (part.pos2[1] > screeny) or (part.pos1[1] < 0) or (part.pos2[1] < 0):
			return 1

		### Player in itself
		#if part.name != 'head':
		#	if (((snake.body_parts[0].pos1[0] <= part.pos1[0] <= snake.body_parts[0].pos2[0]) or (snake.body_parts[0].pos1[0] <= part.pos2[0] <= snake.body_parts[0].pos2[0])) and \
		#		((snake.body_parts[0].pos1[1] >= part.pos1[1]) or (snake.body_parts[0].pos1[1] <= part.pos2[1])) or \
		#	   (((snake.body_parts[0].pos1[1] <= part.pos1[1] <= snake.body_parts[0].pos2[1]) or (snake.body_parts[0].pos1[1] <= part.pos2[1] <= snake.body_parts[0].pos2[1])) and \
		#	    ((snake.body_parts[0].pos1[0] >= part.pos1[0]) or (snake.body_parts[0].pos1[0] <= part.pos2[0])))):
		#		if count < 2:
		#			continue
		#		return 1

	cv2.imshow('Snake', img)

def create_food():
	x1, y1 = random.randint(0, 497), random.randint(0, 497)
	while not (x1%15):
		if x1 + 14 < screenx - 15:
			x1 += 1
		else:
			x1 -= 1
	while not (y1%15):
		if y1 + 14 < screeny - 15:
			y1 -= 1
		else:
			y1 += 1
	return (x1, y1)

class Snake(object):
	def __init__(self):
		head = Body_Part(name='head', pos1=[startx, starty], pos2=[startx + x, starty + y])
		self.body_parts = [head]
	
	def eat_food(self):
		### Going up
		if self.body_parts[-1].vel[1] < 0:
			self.body_parts.append(Body_Part(pos1=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos2[1]], 
											 pos2=[self.body_parts[-1].pos1[0] + x, self.body_parts[-1].pos2[1] + y], 
											 vel=self.body_parts[-1].vel))
		### Going down
		elif self.body_parts[-1].vel[1] > 0:
			self.body_parts.append(Body_Part(pos1=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos1[1] - y], 
											 pos2=[self.body_parts[-1].pos2[0], self.body_parts[-1].pos1[1]], 
											 vel=self.body_parts[-1].vel))
		### Going right
		elif self.body_parts[-1].vel[0] > 0:
			self.body_parts.append(Body_Part(pos1=[self.body_parts[-1].pos1[0] - x, self.body_parts[-1].pos1[1]], 
											 pos2=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos2[1]], 
											 vel=self.body_parts[-1].vel))
		### Going left
		elif self.body_parts[-1].vel[0] < 0:
			self.body_parts.append(Body_Part(pos1=[self.body_parts[-1].pos2[0], self.body_parts[-1].pos1[1]], 
											 pos2=[self.body_parts[-1].pos2[0] + x, self.body_parts[-1].pos2[1]], 
											 vel=self.body_parts[-1].vel))

	def go_right(self):
		if self.body_parts[0].vel != (-15, 0):
			self.body_parts[0].vel = (15, 0)
	def go_left(self):
		if self.body_parts[0].vel != (15, 0):
			self.body_parts[0].vel = (-15, 0)
	def go_up(self):
		if self.body_parts[0].vel != (0, 15):
			self.body_parts[0].vel = (0, -15)
	def go_down(self):
		if self.body_parts[0].vel != (0, -15):
			self.body_parts[0].vel = (0, 15)

class Body_Part(object):
	def __init__(self, pos1, pos2, vel=vel, name='part'):
		self.name = name
		self.pos1 = pos1
		self.pos2 = pos2
		self.vel = vel

if __name__ == '__main__':
	snake = Snake()
	food = create_food()
	counter = 0

	while True:
		img = np.zeros((screenx, screeny, 3), np.uint8)	
		key = cv2.waitKey(450) & 0xFF

		if len(snake.body_parts) > 1:
			for index in range(len(snake.body_parts) - 1, 0, -1):
				snake.body_parts[index].vel = snake.body_parts[index - 1].vel

		if key == 27:
			break

		if key == 119: ### W
			snake.go_up()

		if key == 97:  ### A
			snake.go_left()

		if key == 115: ### S
			snake.go_down()

		if key == 100: ### D
			snake.go_right()

		### Player eats the food
		if ((snake.body_parts[0].pos1[0] <= food[0] <= snake.body_parts[0].pos2[0]) or (snake.body_parts[0].pos1[0] <= food[0] + x <= snake.body_parts[0].pos2[0])) and \
		    ((snake.body_parts[0].pos1[1] <= food[1] <= snake.body_parts[0].pos2[1]) or (snake.body_parts[0].pos1[1] <= food[1] + y <= snake.body_parts[0].pos2[1])):
			food = create_food()
			snake.eat_food()

		response = create_image()

		if response:
			break
		