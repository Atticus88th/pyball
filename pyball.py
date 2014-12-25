import pygame
import random
from enum import Enum

pygame.init()

width = 640
height = 480
ticks_per_second = 60

black = (0, 0, 0)
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("PyBall")
clock = pygame.time.Clock()

brick_image = pygame.image.load('brick.png')
brick_image_size = brick_image.get_rect().size

bricks = []
balls = []
paddles = []

class PowerdropEnum(Enum):
    Nothing = 0
    LoseLife = 1
    GainLife = 2

class MouseButton(Enum):
    Left = 1
    Scroll = 2
    Right = 3

class PowerDropManager:
    def __init__(self, max_powerdrops, creation_delay_seconds):
        self.max_powerdrops = max_powerdrops
        self.powerdrops = []

    def try_create_powerdrop(self, powerdrop_type, (x, y)):
        if len(self.powerdrops) >= self.max_powerdrops:
            print "Too many powerdrops exist."
            return

        power = PowerDrop(powerdrop_type, (x, y))
        self.add_powerdrop(power)

    def add_powerdrop(self, powerdrop):
        self.powerdrops.append(powerdrop)

    def remove_powerdrop(self, powerdrop):
        self.powerdrops.remove(powerdrop)

class PowerDrop:
    def __init__(self, powerdrop, (x, y)):
        self.droptype = powerdrop
        self.image = pygame.image.load('powerdrop_%s.png' %(powerdrop.name.lower()))
        self.id = len(pdm.powerdrops) + 1
        self.x = x
        self.y = y

    def destroy(self):
        print "Destroying powerdrop %s; %s." %(self.id, self.droptype.name)
        pdm.remove_powerdrop(self)

    def tick(self):
        if self.y > height:
            self.destroy()

        self.y += 2

class Ball:
    def __init__(self, (x, y), (dx, dy)):
        self.image = pygame.image.load('ball.png')
        self.id = len(balls) + 1
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.size = self.image.get_rect().size

    def bounds(self):
        x = self.x
        y = self.y
        return (x, x + self.width, y, y + self.height)

    def destroy(self):
        print "Destroying ball %s." %(self.id)
        balls.remove(self)
        # lives -= 1

        # if lives <= 0:
        #     quit_game()

    def tick(self):
        if self.y > height:
            self.destroy()

        self.x += self.dx
        self.y += self.dy

class Paddle:
    def __init__(self, (x, y)):
        self.image = pygame.image.load('paddle.png')
        self.x = x
        self.y = y
        self.size = self.image.get_rect().size

class Brick:
    def __init__(self, powerdrop, (x, y)):
        self.image = pygame.image.load('brick.png')
        self.powerdrop = powerdrop
        self.id = len(bricks) + 1
        self.x = x
        self.y = y
        self.size = self.image.get_rect().size
        self.haspower = powerdrop != PowerdropEnum.Nothing

    def destroy(self):
        print "Destroying brick %s." %(self.id)
        if self.haspower:
            pdm.try_create_powerdrop(self.powerdrop, (self.x, self.y))

        bricks.remove(self)

def brick_at_pos(x, y):
    for b in bricks:
        x1, x2, y1, y2 = bounds_of(b)
        if x1 < x <= x2:
            if y1 < y <= y2:
                return b

    return None

def bounds_of(obj):
    x = obj.x
    y = obj.y
    s = obj.size
    return (x, x + s[0], y, y + s[1])

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

            if etype == pygame.MOUSEMOTION:
                mx, my = e.pos
                p = paddles[0]
                p.x = mx - (p.size[0] / 2)

        display.fill(black)

        for b in bricks:
            draw_image(b.image, (b.x, b.y))

        for p in pdm.powerdrops:
            draw_image(p.image, (p.x, p.y))
            p.tick()

        for b in balls:
            draw_image(b.image, (b.x, b.y))
            b.tick()

        for p in paddles:
            draw_image(p.image, (p.x, p.y))

        pygame.display.update()
        clock.tick(ticks_per_second)

def draw_image(image, (x, y)):
    display.blit(image, (x, y))

def run():
    bricks_per_row = width / brick_image_size[0]

    for row in range(5):
        for col in range(bricks_per_row):
            power = random.choice(list(PowerdropEnum))
            b = Brick(power, (col * brick_image_size[0], row * brick_image_size[1]))
            bricks.append(b)

    ball = Ball((width / 2, height / 2), (0, 2))
    balls.append(ball)

    paddle = Paddle((width / 2, height - 32))
    paddle.x -= paddle.size[0] / 2
    paddles.append(paddle)

    # TODO: When collision is written so we don't have to
    #       destroy bricks manually
    # pygame.mouse.set_visible(False)

    tick()

pdm = PowerDropManager(2, 2)
run()

def quit_game():
    pygame.quit()
    quit()

quit_game()
