# -*- coding: utf-8 -*-
#
# Projet5001: un jeu de survie post-apocalyptique
# Copyright (C) 2014  Équipe Projet5001
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygame
from pygame import Rect
from pygame.locals import *

from basetool import BaseTool


class Weapon(BaseTool):
    def __init__(self, layer_manager, player, name, obj=None):
        super(Weapon, self).__init__(layer_manager, player, name, obj)
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

