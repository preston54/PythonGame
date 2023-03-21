import pygame 
from sys import exit

pygame.init()


width = 800
height = 600
title = "My first pygame"
MAXFPS = 60
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()

test_surface = pygame.Surface((100,200))
test_surface.fill('Red')

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    screen.blit(test_surface,(200,100))

    pygame.display.update()
    clock.tick(MAXFPS)