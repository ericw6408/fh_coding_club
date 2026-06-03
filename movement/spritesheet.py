import pygame

class SpriteSheet:
    def __init__(self, image,width,height,scale,colour):
        self.sheet = image
        self.width = width
        self.height = height
        self.scale = scale
        self.colour = colour

    def get_image(self, frameNum, flip=False):
        image = pygame.Surface((self.width, self.height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frameNum * self.width), 0, self.width, self.height))
        image = pygame.transform.scale(image, (self.width * self.scale, self.height * self.scale))
        image = pygame.transform.flip(image, flip, False)
        image.set_colorkey(self.colour)
        return image