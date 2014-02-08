

import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, screen, image, *groups):
        super(Actor, self).__init__(*groups)
        self.screen = screen
        self.image = pygame.image.load(image)
        self.position = (0, 0)
        self.rect = pygame.rect.Rect(self.position, self.image.get_size())

    def update_position(self):
        pass

    def update(self, dt, game):
        game.tilemap.set_focus(self.rect.x, self.rect.y)