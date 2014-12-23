import pygame

pygame.init()

width = 800
height = 600

black = (0, 0, 0)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyBall")
clock = pygame.time.Clock()

brick_image = pygame.image.load('brick.png')
brick_image_size = brick_image.get_rect().size

class Brick:
	def __init__():
		pass

def tick():
	while True:
		for e in pygame.event.get():
			etype = e.type

			if etype == pygame.QUIT:
				return

		display.fill(black)
		draw_image(brick_image, (0, 0))
		pygame.display.update()
		clock.tick(60)

def draw_image(image, (x, y)):
	display.blit(image, (x, y))

tick()
pygame.quit()
quit()
