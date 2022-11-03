import pygame
from pygame.draw import *

pygame.init()
FPS = 30
screen = pygame.display.set_mode((400, 400))

rect(screen, (200, 200, 200), (0, 0, 400, 400)) # фон
circle(screen, 'yellow', (200, 200), 100) # голова
rect(screen, 'black', (150, 250, 100, 20)) # рот
circle(screen, 'red', (250, 180), 15) # правый глаз
circle(screen, 'black', (250, 180), 7)
circle(screen, 'red', (150, 180), 20) # левый глаз
circle(screen, 'black', (150, 180), 7)
polygon(screen, 'black', ((219, 166), (297, 136), (301, 144), (222, 174)), width=0) # брови
polygon(screen, 'black', ((98, 124), (103, 116), (181, 166), (177, 174)), width=0)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        finished = True

pygame.quit()