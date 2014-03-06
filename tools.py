# -*- coding: utf-8 -*-

import pygame


class Tools(pygame.sprite.Sprite):
    def __init__(self, game, player, name):
        super(Tools, self).__init__()
        self.game = game
        self.name = name
        self.player = player
        self.visible = False

    def update(self, dt, *args):
        pass