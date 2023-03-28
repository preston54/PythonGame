import pygame
from sys import exit

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.input = 'right'
        self.image = pygame.Surface((10,10))
        pygame.Surface.fill(self.image, 'green')
        self.rect = self.image.get_rect(center = (200,200)).move(0,0)

    def move(self, input):
        self.rect = self.rect.move(0, 0)
        if self.input == 'right':
            self.rect.right += self.speed
        if self.input == 'left':
            self.rect.right -= self.speed
        if self.input == 'down':
            self.rect.top += self.speed
        if self.input == 'up':
            self.rect.top -= self.speed
        if self.rect.right > 400:
            self.rect.left = 0
        if self.rect.top > 400-10:
            self.rect.top = 0
        if self.rect.right < 10:
            self.rect.right = 400
        if self.rect.top < 0:
            self.rect.top = 400-10
        
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.input = 'right'
        if keys[pygame.K_LEFT]:
            self.input = 'left'
        if keys[pygame.K_UP]:
            self.input = 'up'
        if keys[pygame.K_DOWN]:
            self.input = 'down'
            

    def update(self):
        self.player_input()
        self.move(self.input)


pygame.init()
screen = pygame.display.set_mode((400,400))
pygame.display.set_caption('Snake 1.0')
clock = pygame.time.Clock()

#background
background = pygame.Surface((400,400))
pygame.Surface.fill(background, (255,255,255))

#groups
snake = pygame.sprite.GroupSingle()
snake.add(Snake())




game_active = True

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(background, (0,0))
    snake.draw(screen)   
    snake.update()     

    pygame.display.update()
    clock.tick(60)

