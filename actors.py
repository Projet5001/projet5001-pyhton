

import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, position, *groups):
        super(Actor, self).__init__(*groups)
        self.image = pygame.image.load(image)
        self.rect = pygame.rect.Rect(position, self.image.get_size())
        self.collision_rect = pygame.rect.Rect(position[0],
                                               position[1] + 20,
                                               20,
                                               20)
        self.savedLastPos = (self.rect.x, self.rect.y)

        #spec of perso
        self.speed = 10
        self.accel = 1
        self.isDoing = "nothing"

    def saveLastPos(self):
        self.savedLastPos = (self.rect.x, self.rect.y)
        self.savedLastCollisionPos = (self.collision_rect.x, self.collision_rect.y)

    def resetPos(self):
        self.rect.x, self.rect.y = self.savedLastPos
        self.collision_rect.x, self.collision_rect.y = self.savedLastCollisionPos

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.collision_rect.move_ip(x, y)

    # this need the dt and game otherwise bug in tmx
    def update(self, dt, game):
        game.tilemap.set_focus(self.collision_rect.x, self.collision_rect.y)
