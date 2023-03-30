import pygame
from pygame.math import Vector2
from random import randint
from sys import exit

class Snake:
    def __init__(self):
        self.body = [Vector2(5,10),Vector2(4,10),Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            snake_rect = pygame.Rect(int(block.x * cell_size),int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, 'green', snake_rect)

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class Apple(): 
    def __init__(self):
        super().__init__()
        self.randomize()
        self.image = pygame.Surface((10,10))
        pygame.Surface.fill(self.image, 'red')
        self.rect = self.image.get_rect(center = (self.xpos,self.ypos))

    def draw_app(self):
        app = pygame.Rect(int(self.xpos * cell_size),int(self.ypos * cell_size),cell_size,cell_size)
        pygame.draw.rect(screen, 'red', app)

    def randomize(self):
        self.xpos = randint(0,cell_count-1)
        self.ypos = randint(0,cell_count-1)
        self.pos = Vector2(self.xpos, self.ypos)

class Main():

    def __init__(self):
        self.snake = Snake()
        self.app = Apple()

    def update(self):
        self.snake.move_snake()
        self.collision()
        self.fail_check()

    def draw_elements(self):
        self.snake.draw_snake()
        self.app.draw_app()

    def collision(self):
        if self.app.pos == self.snake.body[0]:
            self.app.randomize()
            self.snake.add_block()
    
    def fail_check(self):
        if not 0 <= self.snake.body[0].x < cell_count or not 0 <= self.snake.body[0].y < cell_count:
            self.game_over
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        exit()


pygame.init()
cell_size = 20
cell_count = 20
screen = pygame.display.set_mode((cell_size * cell_count, cell_size * cell_count))
pygame.display.set_caption('Snake 1.0')
clock = pygame.time.Clock()

#snake movement timer
screen_update = pygame.USEREVENT + 1
pygame.time.set_timer(screen_update, 150)

#background
background = pygame.Surface((cell_size * cell_count, cell_size * cell_count))
pygame.Surface.fill(background, (255,255,255))

main_game = Main()


game_active = True

while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == screen_update:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1,0)

    screen.blit(background, (0,0))
    main_game.draw_elements()  
    pygame.display.update()
    clock.tick(60)

