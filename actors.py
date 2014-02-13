

import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, position, *groups):
        super(Actor, self).__init__(*groups)
        self.image = pygame.image.load(image)
        self.rect = pygame.rect.Rect(position, self.image.get_size())
        self.savedLastPos = (self.rect.x, self.rect.y)

        #spec of perso
        self.speed = 10
        self.accel = 1
        self.isDoing = "nothing"

    def saveLastPos(self):
        self.savedLastPos = (self.rect.x, self.rect.y)

    def resetPos(self):
        self.rect.x, self.rect.y = self.savedLastPos

    def update_position(self):
        pass

    # this need the dt and game otherwise bug in tmx
    def update(self, dt, game):
        game.tilemap.set_focus(self.rect.x, self.rect.y)