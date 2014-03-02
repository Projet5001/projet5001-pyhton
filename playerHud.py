# -*- coding: utf-8 -*-
import pygame

from lib import tmx

class PlayerHud(tmx.Layer):
    def __init__(self, name, player):
        self.name = name
        self.visible = True
        self.player = player

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        pass

    def draw(self, surface):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render(self.player.name, 1, (255,255,255))
        surface.blit(label, (self.player.collision_rect.x, self.player.collision_rect.y))
