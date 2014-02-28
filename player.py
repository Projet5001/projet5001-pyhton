import actors
import pygame

class Player(actors.Actor):
    def __init__(self, image, position, *groups):
        super(Player, self).__init__(image, position, *groups)
        self.tool_rect = pygame.rect.Rect(position, (5, 30))
        self.speed = 10

    def block(self):
        self.protection = 1
        print "protection"

    def update(self, dt, game):
        game.tilemap.set_focus(self.collision_rect.x, self.collision_rect.y)
        self.protection = 0
