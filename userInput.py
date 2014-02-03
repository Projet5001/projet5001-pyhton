import pygame

class UserInput:
    def __init__(self, config, perso, tilemap):
        self.config = config
        self.perso = perso
        self.tilemap = tilemap #TODO remove if not working
        self.backup = ""

    def update(self):
        # -------- scroll the big map ----------
        pressedkeys = pygame.key.get_pressed()
        if pressedkeys[pygame.K_LEFT]:
            self.perso.position['x'] -= self.config.scrollstepx
        if pressedkeys[pygame.K_RIGHT]:
            self.perso.position['x'] += self.config.scrollstepx
        if pressedkeys[pygame.K_UP]:
            self.perso.position['y'] -= self.config.scrollstepy
        if pressedkeys[pygame.K_DOWN]:
            self.perso.position['y'] += self.config.scrollstepy
        self.tilemap.set_focus(self.perso.position['x'], self.perso.position['y'])

