import pygame
from pygame.locals import *
from basetool import BaseTool
from pygame import Rect

class Weapon(BaseTool):
    def __init__(self, layer_manager, player, name, obj=None):
        super(Weapon, self).__init__(layer_manager, player, name, obj)
        self.hub = self.__followPlayer__()
        #la taille va devoir etre passe en parametre
        self.rect = Rect((self.hub[0], self.hub[1]+8), (5, 100))
        self.image = None

        #ne sera pas hard coder dans le futur
        self.dommage = 1
    @classmethod
    def is_type_for(cls, object_type):
        return object_type == "weapon"

    def is_equippable(self):
        return True

    def draw(self, screen):
        self.hub = self.__followPlayer__()
        pygame.draw.rect(screen, (140,240,130), ((self.hub[0]+20, self.hub[1]+20), (5, 100)))
        self.__update_rect__()

    def __update_rect__(self):
        if self.visible:
            self.hub = self.__followPlayer__()
            self.rect = Rect((self.player.collision_rect[0]+20, self.player.collision_rect[1]+20), (5, 100))
        else:
            self.rect = None

    def handle_collision(self):
        pass

