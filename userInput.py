import pygame


class Keyboard():
    def __init__(self, config, perso):
        self.config = config
        self.perso = perso

    def updateKey(self):
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_LEFT]:
           self.perso.rect.x -= 10
        if pressedkeys[pygame.K_RIGHT]:
            self.perso.rect.x += 10
        if pressedkeys[pygame.K_UP]:
            self.perso.rect.y -= 10
        if pressedkeys[pygame.K_DOWN]:
           self.perso.rect.y += 10