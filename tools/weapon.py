import pygame
from pygame.locals import *
from basetool import BaseTool
from pygame import Rect

class Weapon(BaseTool):
    def __init__(self, layer_manager, player, name, obj=None):
        super(Weapon, self).__init__(layer_manager, player, name, obj)
        self.hub = self.__followPlayer__()
        self.base_mod = 20
        self.mod_left = self.base_mod
        self.mod_top = self.base_mod
        self.size = {}

        self.size['x'] = 5
        self.size['y'] = 50
        self.size['flippe'] = 'v'

        self.rect = Rect((self.hub[0] + self.mod_left, self.hub[1]+self.mod_top), (self.size['y'], self.size['x']))
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
        pygame.draw.rect(screen, (140, 240, 130), ((self.hub[0]+self.mod_left, self.hub[1]+self.mod_top), (self.size['y'], self.size['x'])))

    def __update_rect__(self):
        if self.visible:
            self.rect = Rect((self.player.collision_rect[0]+self.mod_left, self.player.collision_rect[1]+self.mod_top), (self.size['y'], self.size['x']))
        else:
            self.rect = None

    def update(self, dt, *args):
        if self.visible:
            self.__update_rect__()
        else:
            pass

    def receive_event(self, event):
        self.update_rect_box_direction(event)

    def update_rect_box_direction(self, event):
        if event.m == "left":
            if self.size['flippe'] == 'v':
                self.mod_left = self.base_mod - self.size['y']
                self.mod_top = self.base_mod
            else:
                self.flip_size()
                self.mod_left = self.base_mod - self.size['y']
                self.mod_top = self.base_mod

        elif event.m == "right":
            if self.size['flippe'] == 'v':
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod
            else:
                self.flip_size()
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod

        elif event.m == "up":
            if self.size['flippe'] == 'v':
                self.flip_size()
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod - self.size['x']
            else:
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod - self.size['x']

        elif event.m == "down":
            if self.size['flippe'] == 'v':
                self.flip_size()
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod
            else:
                self.mod_left = self.base_mod
                self.mod_top = self.base_mod

    def flip_size(self):
            x = self.size['x']
            y = self.size['y']
            self.size['x'] = y
            self.size['y'] = x
            if self.size['flippe'] == 'h':
                self.size['flippe'] = 'v'
            else:
                self.size['flippe'] = 'h'

    def handle_collision(self):
        pass

