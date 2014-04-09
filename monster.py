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

import random

import actors


class Monster(actors.Actor):
    def __init__(self, name, image, position, *groups):
        super(Monster, self).__init__(name, image, 4, position, *groups)
        self.health = {"hp": 100, "max": 100}
        self.collision_events = []

    def update(self, dt, game):
        if game.blocking:
            return
        self.try_to_get_to_player(game.get_sprite("Max Power").collision_rect)

    def try_to_get_to_player(self, rect):
        delta_x = self.collision_rect.x - rect.x
        delta_y = self.collision_rect.y - rect.y
        deplacement_x = 0
        deplacement_y = 0
        direction_x = ""
        direction_y = ""

        self.saveLastPos()

        # delta_x positif: le perso est vers la gauche.
        # delta_x négatif: le perso est vers la droite.
        if delta_x < 0:
            deplacement_x = 1
            direction_x = "right"
        elif delta_x > 0:
            deplacement_x = -1
            direction_x = "left"

        # delta_y positif: le perso est vers le haut.
        # delta_y négatif: le perso est vers le bas.
        if delta_y < 0:
            deplacement_y = 1
            direction_y = "down"
        elif delta_y > 0:
            deplacement_y = -1
            direction_y = "up"

        if deplacement_x != 0 and deplacement_y != 0:
            if random.choice([0, 1]):
                self.move(deplacement_x, 0, direction_x)
            else:
                self.move(0, deplacement_y, direction_x)
        elif deplacement_x == 0 and deplacement_y != 0:
            self.move(0, deplacement_y, direction_y)
        elif deplacement_x != 0 and deplacement_y == 0:
            self.move(deplacement_x, 0, direction_x)
        else:
            # aucun déplacement nécessaire?
            return

