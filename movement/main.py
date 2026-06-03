import pygame
import spritesheet
from character import Character

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 60

sprite_sheet_image = pygame.image.load('doux.png').convert_alpha()
sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image,24,24,3,(0,0,0))

dino = Character(sprite_sheet.get_image(0),400,300) # setting initial image to be first one, and position to be within the center

BG = (50, 50, 50)    

# Movement variables
speed = 10
standing = False

# Animation booleans 

current_frame = 0
last_update = pygame.time.get_ticks()
ANIMATION_COOLDOWN = 100 #framerate update
is_moving = False
run = True
flip = False



while run:
    # drawing!
    screen.fill(BG)
    dino.draw_self(screen)


    # input handling
    just_pressed = set()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            just_pressed.add(event.key)

    held = pygame.key.get_pressed()
    

    # Movement
    if standing:
        if pygame.K_SPACE in just_pressed:
            dino.set_yvel(-100) # if you are on a ground and jump, you accelerate up wards
        else:
            dino.set_yvel(0)

    if not standing:
        dino.change_y_vel(1) # if you are not on the ground, accelerate downwards
    
    if held[pygame.K_a]:
        flip = True
        dino.set_xvel(-speed)
    elif held[pygame.K_d]:
        flip = False
        dino.set_xvel(speed)
    else:
        if dino.velocity[0] > 0:
            dino.change_x_vel(-1)
        elif dino.velocity[0] < 0:
            dino.change_x_vel(1)

    # updating stuff

    if dino.pos[1] >= SCREEN_HEIGHT - dino.size[1]: 
        dino.set_ypos(SCREEN_HEIGHT - dino.size[1])
        standing = True
    else:
        standing = False

    dino.tick()

    # Animation handling

    current_time = pygame.time.get_ticks()
    if is_moving:
        if current_time - last_update >= ANIMATION_COOLDOWN: #if its been long enough since the last frame:
            current_frame += 1 # increment animation frame
            last_update = current_time # update time variable
            
            current_frame %= 6 # reset every 6 frames
    else:
        current_frame = 0 # reset upon stopping
    
    dino.image = sprite_sheet.get_image(current_frame,flip)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()