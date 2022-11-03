from os import name
import pygame
import json
import pygame.freetype
from pygame.draw import *
from random import randint, random

pygame.init()
FPS = 30
size_x, size_y = 1400, 800
wall = 100
screen = pygame.display.set_mode((size_x, size_y))


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


my_font = pygame.freetype.SysFont( 'Times New Roman', 35)
number_of_unit = 50
speed = 10
price_ball = 1
price_square = 5
score = 0
unit = list()
x1, x2, y1, y2 = wall, size_x - wall, wall, size_y - wall
timer = 0
deadline = 60


class Ball:
    def __init__(self, x1, x2, y1, y2):
        '''Генерация шаров'''
        self.x = randint(x1, x2)
        self.y = randint(y1, y2)
        self.r = randint(10, 50)
        self.vx = random() * speed * 2 - speed
        self.vy = random() * speed * 2 - speed
        self.color = COLORS[randint(0, 5)]

    def move(self, t):
        '''Движ шаров'''
        self.x += self.vx * t
        self.y += self.vy * t

    def vyvod(self):
        '''Рождение шаров'''
        circle(screen, self.color, (self.x, self.y), self.r)

    def sten(self, x1, x2, y1, y2, t):
        '''Отражение от стен'''
        if self.x - self.r + self.vx * t <= x1:
            self.vx = random() * speed
            self.vy = random() * speed * 2 - speed
        if self.x + self.r + self.vx * t >= x2:
            self.vx = -random() * speed
            self.vy = random() * speed * 2 - speed
        if self.y + self.r + self.vy * t >= y2:
            self.vx = random() * speed * 2 - speed
            self.vy = -random() * speed
        if self.y - self.r + self.vy * t <= y1:
            self.vx = random() * speed * 2 - speed
            self.vy = random() * speed

    def blast(self, x, y):
        '''Взрыв шаров'''
        if ((self.x - x) ** 2 + (self.y - y) ** 2) <= self.r ** 2:
            self.Del = unit.pop(i)
            return(price_ball)
        else:
            return(0)


class Square:
    def __init__(self, x1, x2, y1, y2):
        '''Генерация квадратов'''
        self.x = randint(x1, x2)
        self.y = randint(y1, y2)
        self.r = randint(10, 50)
        self.a = 1
        self.vx = random() * speed * 2 - speed
        self.vy = random() * speed * 2 - speed
        self.ax = random() * self.a * 2 - self.a
        self.ay = random() * self.a * 2 - self.a
        self.c = randint(0, 255)
        self.color = [self.c, self.c, self.c]

    def move(self, t):
        '''Движ квадратов'''
        self.vx += self.ax * t
        self.vy += self.ax * t
        self.x += self.vx * t
        self.y += self.vy * t

    def vyvod(self):
        '''Рождение квадратов'''
        if self.color == [255, 255, 255]:
            self.color = [0, 0, 0]
        else:
            for i in range(3):
                self.color[i] += 1
        rect(screen, self.color, (self.x - self.r /
             2, self.y - self.r / 2, self.r, self.r))

    def sten(self, x1, x2, y1, y2, t):
        '''Отражение от стен'''
        self.flag = False
        if self.x - self.r / 2 + self.vx * t <= x1:
            self.vx = random() * speed
            self.vy = random() * speed * 2 - speed
            self.flag = True
        if self.x + self.r / 2 + self.vx * t >= x2:
            self.vx = -random() * speed
            self.vy = random() * speed * 2 - speed
            self.flag = True
        if self.y + self.r / 2 + self.vy * t >= y2:
            self.vx = random() * speed * 2 - speed
            self.vy = -random() * speed
            self.flag = True
        if self.y - self.r / 2 + self.vy * t <= y1:
            self.vx = random() * speed * 2 - speed
            self.vy = random() * speed
            self.flag = True
        if self.flag:
            self.ax = random() * self.a * 2 - self.a
            self.ay = random() * self.a * 2 - self.a

    def blast(self, x, y):
        '''Взрыв квадратов'''
        if abs(self.x - x) <= self.r and abs(self.y - y) <= self.r:
            self.Del = unit.pop(i)
            return(price_square)
        else:
            return(0)


number_of_balls = randint(number_of_unit // 3, number_of_unit * 2 // 3)
number_of_squers = number_of_unit - number_of_balls
for i in range(number_of_balls):
    unit.append(Ball(wall, size_x - wall, wall, size_y - wall))
for i in range(number_of_squers):
    unit.append(Square(wall, size_x - wall, wall, size_y - wall))
pygame.display.update()
clock = pygame.time.Clock()
finished = False
while not finished and timer <= deadline and len(unit) != 0:
    clock.tick(FPS)
    timer += 1 / FPS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            '''Взрыв'''
            for i in range(len(unit)-1, -1, -1):
                score += unit[i].blast(event.pos[0], event.pos[1])
    pygame.display.update()
    screen.fill((255, 255, 255))
    rect(screen, BLACK, (x1, y1, (x2-x1), (y2-y1)))
    my_font.render_to(screen, (20, 20), "score:" + str(score) + "/" +
                      str(number_of_balls * price_ball + number_of_squers * price_square), BLACK)
    my_font.render_to(screen, (size_x - wall - 380, 20), "Осталось времени:" +
                      str(deadline - int(timer)) + "/" + str(deadline), BLACK)
    for i in range(len(unit)):
        unit[i].vyvod()
        unit[i].move(1)
        unit[i].sten(x1, x2, y1, y2, 1)
'''Ввод имени'''
screen.fill(BLACK)
my_font.render_to(screen, (100, 100), "Введите своё имя:", RED)
pygame.display.update()
finished = False
name = ""
while not finished:
    screen.fill(BLACK)
    my_font.render_to(screen, (100, 100), "Введите своё имя:", RED)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                finished = True
            elif event.key == pygame.K_BACKSPACE:
                name = name[:-1]
            else:
                name += pygame.key.name(event.key)
        my_font.render_to(screen, (100, 140), name, RED)
        pygame.display.update()

with open(r"D:\Шаров\tabl2.json") as f:
    data = json.load(f)
data[name] = score
if len(unit) == 0:
    rect(screen, RED, (0, 0, size_x, size_y))
    my_font.render_to(screen, (20, 20),
                      name + " - you're cool", (255, 255, 255))
else:
    rect(screen, RED, (0, 0, size_x, size_y))
    my_font.render_to(screen, (20, 20),
                      name + " - You're cool too ", (255, 255, 255))
h = 50
"""Вывод таблицы рекордов"""
for k, v in data.items():
    my_font.render_to(screen, (20, h), k + ":=" + str(v), (255, 255, 255))
    h += 30
pygame.display.update()
finished = False
while not finished:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
with open(r"D:\Шаров\tabl2.json", 'w') as f:
    json.dump(data, f)
pygame.quit()
