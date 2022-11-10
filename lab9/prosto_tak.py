import math
import random
from random import choice
import pygame
from pygame.draw import *
import pygame.freetype


FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball
        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.g = -3
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.
        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        # FIXME
        self.vy += self.g
        if not(0 < self.x - self.r + self.vx < 800):
            self.vx = - self.vx / 2
        if not(0 < self.y - self.r - self.vy < 450):
            self.vy = - self.vy / 2
        self.live -= 1
        self.x += self.vx
        self.y -= self.vy

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.
        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1]-new_ball.y), (event.pos[0]-new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = - self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan((event.pos[1]-450) / (event.pos[0]-20))
        if self.f2_on:
            self.color = RED
        else:
            self.color = GREY

    def draw(self):
        '''Прорисовка пушки'''
        line(screen, self.color, (20, 450), (math.cos(self.an) *
                                             self.f2_power + 20, math.sin(self.an) * self.f2_power + 450), width=7)

    def power_up(self):
        '''Накапливание силы'''
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
                self.color = GREY
            else:
                self.color = RED
        else:
            self.color = GREY


class Target:
    def __init__(self):

        self.points = 0
        self.live = 1
        self.new_target()

    def new_target(self):
        """ Инициализация новой цели. """
        self.x = random.randint(600, 780)
        self.y = random.randint(300, 450)
        self.r = random.randint(5, 50)
        self.color = RED

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def draw(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.
        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        # FIXME
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            obj.live = 0
            return True
        else:
            return False


class moving:
    def __init__(self):

        self.points = 0
        self.live = 1
        self.new_target()

    def hit(self, points=1):
        """Попадание шарика в цель."""
        self.points += points

    def hittest(self, obj):
        if (-obj.r <= obj.x - self.x <= self.r + obj.r) and (-obj.r <= obj.y - self.y <= self.r  + obj.r):
            obj.live = 0
            return True
        else:
            return False

    def move(self):
        if not(0 <= self.y <= HEIGHT):
            self.speed *= -1
        self.y += self.speed

    def new_target(self):
        self.x = random.randint(500, 600)
        self.y = random.randint(200, 450)
        self.r = random.randint(50, 70)
        self.speed = random.random() * 15 - 7.5

    def draw(self):
        circle(screen, BLUE, (self.x, self.y), self.r)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
bullet = 0
balls = []

clock = pygame.time.Clock()
gun = Gun(screen)
target = Target()
finished = False
m = moving()
while not finished:
    screen.fill(WHITE)

    m.draw()
    my_font = pygame.freetype.SysFont(
        'Times New Roman', 25)  # задание параметров текста
    my_font.render_to(screen, (20, 20),
                      "Количество очков " + str(target.points + m.points), BLACK)
    gun.draw()
    target.draw()
    for b in balls:
        b.draw()
    pygame.display.update()

    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
    m.move()
    for i in range(len(balls)-1, -1, -1):
        b = balls[i]
        b.move()
        if m.hittest(b) and m.live:
            m.live = 1
            m.hit(5)
            m.new_target()
        if target.hittest(b):
            target.live = 1
            target.hit()
            target.new_target()
        if b.live <= 0:
            balls.pop(i)
    gun.power_up()
pygame.quit()