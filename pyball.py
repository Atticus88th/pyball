import pygame
import random
from enum import Enum

pygame.init()

width = 800
height = 600

black = (0, 0, 0)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyBall")
clock = pygame.time.Clock()

brick_image = pygame.image.load('brick.png')
brick_image_size = brick_image.get_rect().size

bricks = []

class Powerdrop(Enum):
	Nothing = 0
	LoseLife = 1
	GainLife = 2

class Brick:
	def __init__(self, powerdrop, (x, y)):
		self.image = pygame.image.load('brick.png')
		self.powerdrop = powerdrop
		self.id = len(bricks) + 1
		self.x = x
		self.y = y
		self.haspower = powerdrop != Powerdrop.Nothing

	def drop_power():
		pass

def tick():
	while True:
		for e in pygame.event.get():
			etype = e.type

			if etype == pygame.QUIT:
				return

		display.fill(black)

		for b in bricks:
			draw_image(b.image, (b.x, b.y))

		pygame.display.update()
		clock.tick(60)

def draw_image(image, (x, y)):
	display.blit(image, (x, y))

def init():
	bricks_per_row = width / brick_image_size[0]

	for row in range(0, 5):
		for col in range(0, bricks_per_row):
			power = random.choice(list(Powerdrop))
			b = Brick(power, (col * brick_image_size[0], row * brick_image_size[1]))
			bricks.append(b)

	# Visual test
	for b in bricks:
		if not b.haspower:
			bricks.remove(b)

init()
tick()
pygame.quit()
quit()
