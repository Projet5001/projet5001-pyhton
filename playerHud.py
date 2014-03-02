# -*- coding: utf-8 -*-
import pygame

from lib import tmx

class PlayerHud(tmx.Layer):
    def __init__(self, name, visible):
        self.name = name
        self.visible = visible

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        pass

    def draw(self, surface):
        myfont = pygame.font.SysFont("monospace", 15)
        label = myfont.render("Some text!", 1, (255,255,0))
        surface.blit(label, (100, 100))