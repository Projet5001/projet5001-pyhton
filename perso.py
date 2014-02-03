import pygame

class Perso(pygame.sprite.Sprite):
    def __init__(self, screen, image):
        super(Perso, self).__init__()
        self.screen = screen
        self.image = pygame.image.load(image)
        self.position = {'x': 320, 'y': 240}


    def update(self):
        self.screen.blit(self.image, (self.position['x'], self.position['y']))
