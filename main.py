import cv2
import numpy as np
import random

x, y, vel = 15, 15, (15, 0)
startx, starty = 100, 100
screenx, screeny = 600, 600

def create_image():

	for index, part in enumerate(snake.body_parts):

		### Move body to the next frame
		part.pos1[0] += part.vel[0]
		part.pos1[1] += part.vel[1]
		part.pos2[0] += part.vel[0]
		part.pos2[1] += part.vel[1]

		pos1, pos2 = part.pos1, part.pos2
		cv2.rectangle(img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 255, 0), -1)

		### Player outside window
		if (part.pos1[0] > screenx) or (part.pos2[0] > screenx) or (part.pos1[0] < 0) or (part.pos2[0] < 0) or \
		   (part.pos1[1] > screeny) or (part.pos2[1] > screeny) or (part.pos1[1] < 30) or (part.pos2[1] < 30):
			return 1

		### Player in itself
		if index > 2:
			if ((snake.body_parts[0].pos1[0] == part.pos1[0] and part.pos2[0] == snake.body_parts[0].pos2[0])):
				if ((snake.body_parts[0].pos1[1] == part.pos1[1] and part.pos2[1] ==  snake.body_parts[0].pos2[1])):
					return 1

	cv2.rectangle(img, (0, 0), (screenx, 30), (255, 255, 255), -1) ### Blank bar at the top
	cv2.rectangle(img, (food[0], food[1]), (food[0] + 12, food[1] + 12), (0, 255, 255), -1) ### Yellow food
	cv2.putText(img=img, text=f"Score: {score}", fontFace=cv2.FONT_HERSHEY_SIMPLEX, org=(25, 25), fontScale=1, color=(0, 0, 0), lineType=1, thickness=2) ### Score
	cv2.imshow('Snake', img) ### Shows the image

def create_food():
	x1, y1 = random.randint(0, screenx - x), random.randint(35, screeny - y)
	return x1, y1

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

	### Update direction if the head is not going the opposite direction
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
	score = 0

	while True:
		img = np.zeros((screenx, screeny, 3), np.uint8)	
		key = cv2.waitKey(250) & 0xFF

		### Updates body position
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
			score += 1

		### Create the image
		response = create_image()

		if response:
			break
		