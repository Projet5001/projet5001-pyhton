import pygame
from pygame.locals import *
from basetool import BaseTool
from pygame import Rect

class Weapon(BaseTool):
    def __init__(self, game, player, name, obj=None):
        super(Weapon, self).__init__(game, player, name, obj)
        self.hub = self.__followPlayer__()
        self.rect = Rect((self.hub[0], self.hub[1]+8), (5, 100))
        self.image = None

    @classmethod
    def is_type_for(cls, object_type):
        return object_type == "weapon"

    def is_equippable(self):
        return True

    def draw(self, screen):
        self.hub = self.__followPlayer__()
        pygame.draw.rect(screen, (140,240,130), ((self.hub[0], self.hub[1]+8), (5, 100)))

    def update(self, dt, *args):
        self.hub = self.__followPlayer__()
        self.rect = Rect((self.player.collision_rect[0], self.player.collision_rect[1]+8), (5, 100))

    def handle_collision(self):
        pass

