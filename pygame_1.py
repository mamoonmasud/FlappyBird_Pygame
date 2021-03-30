# PyGame

import pygame
import sys
import random


def draw_fl():
    screen_dimen.blit(bottom_surf, (bot_x_pos, 900))
    screen_dimen.blit(bottom_surf, (bot_x_pos + 576 , 900))
    
def create_pipe():
    ran_p_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surf.get_rect(midtop= (700, ran_p_pos))
    top_pipe = pipe_surf.get_rect(midbottom= (700, ran_p_pos - 300))
    return [bottom_pipe, top_pipe]

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= 4
    return pipes

def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= 1024:
            screen_dimen.blit(pipe_surf, p)
        else:
            flip_p = pygame.transform.flip(pipe_surf, False, True )
            screen_dimen.blit(flip_p , p )

def collision_check(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            death_s.play()
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, bird_mov*-3, 1)
    return new_bird

def bird_animate():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_show(game_state):
    if game_state == 'main_game':

        score_surf = game_font.render(str(int(score)), True, (255, 255, 220))
        score_rect = score_surf.get_rect(center = (288, 100))
        screen_dimen.blit(score_surf, score_rect)
    if game_state == 'game_over':
        score_surf = game_font.render(f'Score : {int(score)}', True, (255, 255, 220))
        score_rect = score_surf.get_rect(center = (288, 100))
        screen_dimen.blit(score_surf, score_rect)
        
        high_score_surf = game_font.render(f'High Score : {int(high_score)}', True, (255, 255, 220))
        high_score_rect = score_surf.get_rect(center = (288, 800))
        screen_dimen.blit(high_score_surf, high_score_rect)

def score_update(score, high_score):
    if score> high_score:
        high_score = score
    return high_score



#initializing the pygame module 

pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer= 1024)
pygame.init()

#Setting the screen height and width (The canvas will be created of this dimension)
screen_dimen = pygame.display.set_mode(( 576,1024)) 

# Setting a random caption title for your pygame graphical window.
pygame.display.set_caption("Testing 101")

#clock object for setting the frame rate
clock = pygame.time.Clock()

# Font
game_font = pygame.font.Font('flappy-bird-assets-master/04B_19.ttf', 40)
#Game Variables
gravity = 0.25
bird_mov =0

game_active = True

score = 0
high_score = 0

#Creating Surfaces to load the images on to
bg_surf = pygame.image.load('flappy-bird-assets-master/sprites/background-day.png').convert()
bg_surf = pygame.transform.scale2x(bg_surf)

bottom_surf= pygame.image.load('flappy-bird-assets-master/sprites/base.png').convert()
bottom_surf = pygame.transform.scale2x(bottom_surf)

bot_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-downflap.png').convert_alpha())
bird_midflap  = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha())
bird_upflap   = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha())
bird_frames   = [ bird_upflap, bird_midflap, bird_downflap, bird_midflap]

bird_index = 1
bird_surf = bird_frames[bird_index]
bird_rect = bird_surf.get_rect(center = (100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)
#Importing Bird Image

# bird_surf = pygame.image.load('flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha()
# bird_surf =pygame.transform.scale2x(bird_surf)
# bird_rect = bird_surf.get_rect(center =(100, 512))

# Importing Pipes
pipe_surf = pygame.image.load('flappy-bird-assets-master/sprites/pipe-green.png')
pipe_surf =pygame.transform.scale2x(pipe_surf)
pipe_list = []
pipe_height = [400, 500, 600, 700, 800]

game_over_surf = pygame.transform.scale2x(pygame.image.load('flappy-bird-assets-master/sprites/message.png').convert_alpha())
game_over_rect = game_over_surf.get_rect(center = (288, 512))
SPAWN_PIPE= pygame.USEREVENT
pygame.time.set_timer(SPAWN_PIPE, 1200)

flap_s = pygame.mixer.Sound('sounds/sfx_wing.wav')
death_s =pygame.mixer.Sound('sounds/sfx_die.wav')
score_s = pygame.mixer.Sound('sounds/sfx_point.wav')
score_s_countdown  = 100


# Perpetual Loop
while True:
    #This follows the event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() #For shutting down the 
            
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_mov =0
                bird_mov -= 10
                flap_s.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active= True
                pipe_list.clear()
                bird_rect.center = (100,512)
                bird_mov =0
                score =0
        if event.type == SPAWN_PIPE:
            pipe_list.extend(create_pipe())
            
        if event.type == BIRDFLAP:
            if bird_index < 3:
                bird_index +=1
            else:
                bird_index = 0
            bird_surf ,bird_rect = bird_animate()
            
            
    #Updating the screen
    screen_dimen.blit(bg_surf, (0, 0))
    if game_active:
        # Bird
        bird_mov += gravity
        
        rot_bird = rotate_bird(bird_surf)
        
        bird_rect.centery += bird_mov
        screen_dimen.blit(rot_bird, bird_rect)
        
        # Checking Collisions
        game_active = collision_check(pipe_list)
        #Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        score += 0.01
        score_show('main_game')
        score_s_countdown -=1
        if score_s_countdown <=0:
            score_s.play()
            score_s_countdown= 100
    else:
        screen_dimen.blit(game_over_surf, game_over_rect)
        high_score= score_update(score, high_score)
        score_show('game_over')
        
    #Floor
    bot_x_pos -= 4
     
    draw_fl()
    if bot_x_pos <= -576:
        bot_x_pos = 0
    pygame.display.update()
    #Limitng the Frame Rate
    clock.tick(120)