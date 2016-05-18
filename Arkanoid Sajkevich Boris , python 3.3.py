# -*- coding: utf-8 -*-
import math
import pygame
# Задаем цвета
white = (255, 255, 255)
green = (0, 100, 0)
gray = (49 , 79 , 79)
pale = (0,206,209)
# Размер разбиваемых блоков
block_width = 27
block_height = 24

class Block(pygame.sprite.Sprite):
    def __init__(self, color, x, y):
        super().__init__()
        self.image = pygame.Surface([block_width, block_height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ball(pygame.sprite.Sprite):
    # скорость в пикселях
    speed = 11.0
    x = 1.0
    y = 170.0
    direction = 190
    width = 9
    height = 9

    # В Python есть метод super(), который обычно применяется к объектам.
    # Его главная задача это возможность использования в классе потомке, методов класса-родителя.
    # По аналогии с PHP5 нечто вроде parrent::__construct()
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
    def update(self):
        direction_radians = math.radians(self.direction)
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        self.rect.x = self.x
        self.rect.y = self.y

        # шарик прыгает вверху экрана
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
        # шарик прыгает слева
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
        # шарик прыгает справа
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        if self.y > 600:
            return True
        else:
            return False


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
# задаем размеры слайдера
        self.width = 105
        self.height = 20
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((gray))

        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight-self.height

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > self.screenwidth - self.width:
            self.rect.x = self.screenwidth - self.width

pygame.init()

# создаем экран размер 800 на 600
screen = pygame.display.set_mode([800, 600])

#название игры
pygame.display.set_caption('Arkanoid,kursovaya :)')

# управление мышкой
pygame.mouse.set_visible(0)

font = pygame.font.Font(None, 36)

background = pygame.Surface(screen.get_size())

# создаем спрайты
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()

player = Player()
allsprites.add(player)

# создаем мяч
ball = Ball()
allsprites.add(ball)
balls.add(ball)

top = 80

# номер блоков для создания
blockcount = 32

for row in range(5):
    for column in range(0, blockcount):
        block = Block(green, column * (block_width + 2) + 1, top)
        blocks.add(block)
        allsprites.add(block)
    top += block_height + 2

clock = pygame.time.Clock()
game_over = False
exit_program = False

while not exit_program:
    clock.tick(30)
    screen.fill(pale)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
    if not game_over:
        player.update()
        game_over = ball.update()
    if game_over:
        text = font.render("Proigrali (Game over)", True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
    if pygame.sprite.spritecollide(player, balls, False):
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    if len(deadblocks) > 0:
        ball.bounce(0)
        if len(blocks) == 0:
            game_over = True
    allsprites.draw(screen)
    pygame.display.flip()

pygame.quit()