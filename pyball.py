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
powerdrops = []

class PowerdropEnum(Enum):
    Nothing = 0
    LoseLife = 1
    GainLife = 2

class MouseButton(Enum):
    Left = 1
    Scroll = 2
    Right = 3

class PowerDrop:
    def __init__(self, powerdrop, (x, y)):
        self.droptype = powerdrop
        self.image = pygame.image.load('powerdrop_%s.png' %(powerdrop.name.lower()))
        self.id = len(powerdrops) + 1
        self.x = x
        self.y = y

    def destroy(self):
        print "Destroying powerdrop %s; %s." %(self.id, self.droptype.name)
        powerdrops.remove(self)

    def tick(self):
        if self.y > height:
            self.destroy()

        self.y += 2

class Brick:
    def __init__(self, powerdrop, (x, y)):
        self.image = pygame.image.load('brick.png')
        self.powerdrop = powerdrop
        self.id = len(bricks) + 1
        self.x = x
        self.y = y
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]
        self.haspower = powerdrop != PowerdropEnum.Nothing

    def bounds(self):
        x = self.x
        y = self.y
        return (x, x + self.width, y, y + self.height)

    def destroy(self):
        print "Destroying brick %s." %(self.id)
        if self.haspower:
            power = PowerDrop(self.powerdrop, (self.x, self.y + 20))
            powerdrops.append(power)

        bricks.remove(self)

def brick_at_pos(x, y):
    for b in bricks:
        x1, x2, y1, y2 = b.bounds()
        if x1 < x <= x2:
            if y1 < y <= y2:
                return b

    return None

def tick():
    while True:
        for e in pygame.event.get():
            etype = e.type

            if etype == pygame.QUIT:
                return

            if etype == pygame.MOUSEBUTTONDOWN:
                mx, my = e.pos

                if e.button == MouseButton.Right.value:
                    clicked = brick_at_pos(mx, my)

                    if clicked is not None:
                        clicked.destroy()

        display.fill(black)

        for b in bricks:
            draw_image(b.image, (b.x, b.y))

        for p in powerdrops:
            draw_image(p.image, (p.x, p.y))
            p.tick()

        pygame.display.update()
        clock.tick(60)

def draw_image(image, (x, y)):
    display.blit(image, (x, y))

def init():
    bricks_per_row = width / brick_image_size[0]

    for row in range(5):
        for col in range(bricks_per_row):
            power = random.choice(list(PowerdropEnum))
            b = Brick(power, (col * brick_image_size[0], row * brick_image_size[1]))
            bricks.append(b)

    # Visual test
    # for b in bricks:
    # 	if not b.haspower:
    # 		bricks.remove(b)

init()
tick()
pygame.quit()
quit()
