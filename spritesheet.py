#image_test.py
import sys
import pygame



resolution = [1000,500]

clock = pygame.time.Clock()
screen = pygame.display.set_mode(resolution)
running = True

image_path = "C:\\Users\\afren\\desktop\\code\\img\\spritesheet.png"
image = pygame.image.load(image_path)

# download a spritesheet image, then right click -> show more options -> copy as path


sprite_width = 32
sprite_height = 32
empty_guy = pygame.Surface((sprite_width,sprite_height),pygame.SRCALPHA)


# Given a row and column, returns the top left coordinate of that sprite
def get_dimensions(row,column,width=32,height=32):
    left_coordinate = (column-1)*width
    top_coordinate = (row-1)*height
    return [left_coordinate,top_coordinate]

# Given the top left coordinate of an image and a surface, blits the corresponding stuff
def blit_image(coordinate ,surface:pygame.Surface, width=sprite_width, height = sprite_height):
    surface.blit(image,pygame.Rect(coordinate[0],coordinate[1],width,height))
    
row = 1
column = 1

x_pos = 5
y_pos = 5

resized = pygame.Surface([128,128])

frame = 0

while running:
    clock.tick(5)
    screen.fill((50, 0, 0))

    empty_guy.fill((0, 0, 0, 0))
    col = (frame % 10) + 1  # 1-based, cycles 1–10
    source_rect = pygame.Rect(*get_dimensions(row, col), sprite_width, sprite_height)
    empty_guy.blit(image, (0, 0), source_rect)  # ← fixed
    
    resized = pygame.transform.scale(empty_guy, [128, 128])
    screen.blit(resized, (x_pos, y_pos))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    x_pos += 1
    y_pos += 1
    pygame.display.flip()
    frame += 1

