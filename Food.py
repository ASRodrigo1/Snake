import numpy as np

class Food():

	def __init__(self, limitx, limity, food_size):
		self.x = np.random.randint(0, limitx - food_size)
		self.y = np.random.randint(0, limity - food_size)