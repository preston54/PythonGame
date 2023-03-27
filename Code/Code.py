import pygame 
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.3)
        player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.image = self.player_walk[self.player_index] 
        self.rect = self.image.get_rect(midbottom = (80,300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
    
    def player_animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk): self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.player_animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_surf_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
            fly_surf_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
            self.frames = [fly_surf_1,fly_surf_2]
            y_pos = 210
        else:
            snail_surf_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_surf_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_surf_1,snail_surf_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100),y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    curr_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(f'Score: {curr_time}',False,(64,64,64))
    score_rec = score_surf.get_rect(center = (400,50))
    screen.blit(score_surf,score_rec)

    return curr_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 5


            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf,obstacle_rect)
            else:
                screen.blit(fly_surf,obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite,obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True

def player_animation():
    global player_surf,player_index

    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

width = 800
height = 400
title = "My first pygame"
MAXFPS = 60
game_active = False
start_time = 0
score = 0

pygame.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption(title)
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf' ,50)
sky_surf = pygame.image.load('graphics/Sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops = -1)
bg_music.set_volume(0.3)
# text_surf = test_font.render('My game', False, (64,64,64))
# text_rect = text_surf.get_rect(center = (400,50))

#obstacles
snail_surf_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_surf_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_frames = [snail_surf_1,snail_surf_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]
fly_surf_1 = pygame.image.load('graphics/fly/Fly1.png').convert_alpha()
fly_surf_2 = pygame.image.load('graphics/fly/Fly2.png').convert_alpha()
fly_frames = [fly_surf_1,fly_surf_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]
obstacle_rect_list = []

player_grav = 0
player_walk_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80,300))

player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()


#Intro screen
player_stand = pygame.image.load('graphics/player/player_stand.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400,200))

title_msg = test_font.render('Running man', False, '#072530' )
title_msg_rect = title_msg.get_rect(center = (400,50))

instruc_msg = test_font.render('Press space to start', False, '#072530')
instruc_msg_rect = instruc_msg.get_rect(center = (400, 350))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 500)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEMOTION:
                if player_rect.collidepoint(event.pos):
                    print('collided')

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_grav = -20
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 1000) 

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail'])))
                #old obstacle creation
                # if randint(0,2):
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),300)))
                # else:
                #     obstacle_rect_list.append(snail_surf.get_rect(bottomright = (randint(900,1100),210)))
            if event.type == snail_timer:
                if snail_frame_index == 0: snail_frame_index = 1
                else: snail_frame_index = 0
                snail_surf = snail_frames[snail_frame_index]
            if event.type == fly_timer:
                if fly_frame_index == 0: fly_frame_index = 1
                else: fly_frame_index = 1
                fly_surf = fly_frames[fly_frame_index]


    if game_active:
        #creating background
        screen.blit(sky_surf,(0,0))
        screen.blit(ground_surf,(0,300))
        # pygame.draw.rect(screen, '#c0e8ec', text_rect)
        # pygame.draw.rect(screen, '#c0e8ec', text_rect, 10)
        # screen.blit(text_surf,text_rect)
        score = display_score()

        #snail movement and sprite
        # snail_rect.x -= 4
        # if snail_rect.right <= 0:
        #     snail_rect.left = 800
        # screen.blit(snail_surf,snail_rect)  


        #obstacle movement
        # obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        #player sprite  
        # player_grav += 1
        # player_rect.y += player_grav
        # if player_rect.bottom >= 300: player_rect.bottom = 300
        # player_animation()
        # screen.blit(player_surf,player_rect)
        player.draw(screen)
        player.update()
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision between rects -- colliderect
        game_active = collision_sprite()
        
    else:

        obstacle_rect_list.clear()
        screen.fill('#43A1C3')
        screen.blit(player_stand,player_stand_rect)
        screen.blit(title_msg,title_msg_rect)
        score_msg = test_font.render(f'Score: {score}', False, '#072530')
        score_msg_rect = score_msg.get_rect(center = (400,350))
        player_rect.midbottom = (80,300)
        player_gravity = 0
        
        if score == 0:
            screen.blit(instruc_msg, instruc_msg_rect)
        else:
            screen.blit(score_msg,score_msg_rect)
    
    #jump encoding
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_SPACE]:
    #     print('jump')

    # #mouse collision -- collidepoint
    # mous_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mous_pos):
    #     pygame.mouse.get_pressed()


    pygame.display.update()
    clock.tick(MAXFPS)