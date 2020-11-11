import numpy as np
import random
import cv2
from BodyPart import BodyPart
from Food import Food

FOOD_SIZE = 15
BODY_PART_SIZE = 15
SCREENX = 600
SCREENY = 600

def transform(img):
	img = cv2.resize(img, (84, 84)) ### Resizing the image
	img = np.reshape(img, (3, 84, 84)) ### Channels first
	img /= 255.0

	return img

class Game():

	def __init__(self):
		self.observation_space_shape = (84, 84)
		self.action_space_n = 4

	def reset(self):

		self.score = 0
		### Random position to put the head
		startX = np.random.randint(100, 500)
		startY = np.random.randint(100, 500)

		### Random head velocity
		vel = random.choice([[15, 0], [-15, 0], [0, 15], [0, -15]])

		### Create the head and store it in the list of body parts
		self.body_parts = []
		head = BodyPart(pos1=[startX, startY], pos2=[startX + BODY_PART_SIZE, startY + BODY_PART_SIZE], 
			            vel=vel, name='head')

		self.body_parts.append(head)

		### Create the food
		self.food = Food(limitx=SCREENX, limity=SCREENY, food_size=FOOD_SIZE)

		### Create the image and return it
		self.create_image()

		### Draw objects on the image
		self.draw()

		### Return image ready to train
		return transform(self.img)

	def draw(self):

		### Food
		cv2.rectangle(self.img, (self.food.x, self.food.y), (self.food.x + FOOD_SIZE, self.food.y + FOOD_SIZE), 
			         (0, 255, 255), -1)

		### Updates body position
		if len(self.body_parts) > 1:
			for index in range(len(self.body_parts) - 1, 0, -1):
				self.body_parts[index].vel = self.body_parts[index - 1].vel

		### Draw body parts
		for index, part in enumerate(self.body_parts):

			### Move part to next position
			part.pos1[0] += part.vel[0]
			part.pos1[1] += part.vel[1]
			part.pos2[0] += part.vel[0]
			part.pos2[1] += part.vel[1]

			pos1, pos2 = part.pos1, part.pos2

			if not index: ### Head in a different color
				cv2.rectangle(self.img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (255, 0, 0), -1)
			else:
				cv2.rectangle(self.img, (pos1[0], pos1[1]), (pos2[0], pos2[1]), (0, 255, 0), -1)

	def create_image(self):

		self.img = np.zeros((SCREENX, SCREENY, 3), np.float32)

	def render(self):
		
		cv2.imshow('Snake', self.img) ### Display the frame
		key = cv2.waitKey(250)

	def step(self, action):

		### 0 -> Go Right
		### 1 -> Go Left
		### 2 -> Go Up
		### 3 -> Go Down
		if not action:
			self.go_right()
		elif action == 1:
			self.go_left()
		elif action == 2:
			self.go_up()
		elif action == 3:
			self.go_down()
		else:
			return "Action must be in range [0, 3]"

		### Check if the player ate the food
		self.check_eat()

		### Create the next frame
		self.create_image()
		self.draw()
		n_state = transform(self.img)

		### Compute reward
		reward = self.compute_reward()

		### Compute done
		done = True if not reward else False

		return n_state, reward, done

	def sample_action(sef):
		return np.random.randint(0, 4)

	def compute_reward(self):
		
		if self.check_lost():
			return 0
		else:
			return 1

	def check_lost(self):
		
		for index, part in enumerate(self.body_parts):
			### Player outside window
			if (part.pos1[0] > SCREENX) or (part.pos2[0] > SCREENX) or (part.pos1[0] < 0) or (part.pos2[0] < 0) or \
			   (part.pos1[1] > SCREENY) or (part.pos2[1] > SCREENY) or (part.pos1[1] < 0) or (part.pos2[1] < 0):
				return 1

			### Player in itself
			if index > 2:
				if ((self.body_parts[0].pos1[0] == part.pos1[0] and part.pos2[0] == self.body_parts[0].pos2[0])):
					if ((self.body_parts[0].pos1[1] == part.pos1[1] and part.pos2[1] ==  self.body_parts[0].pos2[1])):
						return 1
		return 0

	def check_eat(self):
		
		### Player eats the food
		if ((self.body_parts[0].pos1[0] <= self.food.x <= self.body_parts[0].pos2[0]) or \
			(self.body_parts[0].pos1[0] <= self.food.x + FOOD_SIZE <= self.body_parts[0].pos2[0])) and \
		    ((self.body_parts[0].pos1[1] <= self.food.y <= self.body_parts[0].pos2[1]) or \
		    (self.body_parts[0].pos1[1] <= self.food.y + FOOD_SIZE <= self.body_parts[0].pos2[1])):

			self.food = Food(limitx=SCREENX, limity=SCREENY, food_size=FOOD_SIZE)
			self.grow()
			self.score += 1

	def grow(self):

		### Going up
		if self.body_parts[-1].vel[1] < 0:
			self.body_parts.append(BodyPart(pos1=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos2[1]], 
											 pos2=[self.body_parts[-1].pos1[0] + BODY_PART_SIZE, self.body_parts[-1].pos2[1] + BODY_PART_SIZE], 
											 vel=self.body_parts[-1].vel))
		### Going down
		elif self.body_parts[-1].vel[1] > 0:
			self.body_parts.append(BodyPart(pos1=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos1[1] - BODY_PART_SIZE], 
											 pos2=[self.body_parts[-1].pos2[0], self.body_parts[-1].pos1[1]], 
											 vel=self.body_parts[-1].vel))
		### Going right
		elif self.body_parts[-1].vel[0] > 0:
			self.body_parts.append(BodyPart(pos1=[self.body_parts[-1].pos1[0] - BODY_PART_SIZE, self.body_parts[-1].pos1[1]], 
											 pos2=[self.body_parts[-1].pos1[0], self.body_parts[-1].pos2[1]], 
											 vel=self.body_parts[-1].vel))
		### Going left
		elif self.body_parts[-1].vel[0] < 0:
			self.body_parts.append(BodyPart(pos1=[self.body_parts[-1].pos2[0], self.body_parts[-1].pos1[1]], 
											 pos2=[self.body_parts[-1].pos2[0] + BODY_PART_SIZE, self.body_parts[-1].pos2[1]], 
											 vel=self.body_parts[-1].vel))

	def go_right(self):

		if self.body_parts[0].vel != (-15, 0):
			self.body_parts[0].vel = [15, 0]

	def go_left(self):

		if self.body_parts[0].vel != (15, 0):
			self.body_parts[0].vel = [-15, 0]

	def go_up(self):

		if self.body_parts[0].vel != (0, 15):
			self.body_parts[0].vel = [0, -15]

	def go_down(self):

		if self.body_parts[0].vel != (0, -15):
			self.body_parts[0].vel = [0, 15]