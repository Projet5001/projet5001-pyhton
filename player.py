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

import actors
import tools


class Player(actors.Actor):
    def __init__(self, name, image, position, *groups):
        super(Player, self).__init__(name, image, 12, position, *groups)
        self.speed = 10

        #pour les test du HUD
        self.name = "Max Power"
        self.level = 99
        self.health = {"hp": 27, "max": 38}

    def block(self):
        #methode qui aura plus de fonctionalié plus tard
        self.protection = 1

    def update(self, dt, game):
        game.tilemap.set_focus(self.collision_rect.x, self.collision_rect.y)
        self.protection = 0
