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
from pygame.locals import *

from eventManager import EventEnum

from basetool import BaseTool


class TransitionObject(BaseTool):
    def __init__(self, layer_manager, player, name, obj=None):
        super(TransitionObject, self).__init__(layer_manager, player, name, obj)

    @classmethod
    def is_type_for(cls, object_type):
        allowed = ["porte", "escalier"]
        if object_type in allowed:
            return True
        return False

    def handle_collision(self):
        self.player.resetPos()

        # fire new event for transition (otherwise there is no way to call effectuer_transition)
        # TODO: rework events into own class.
        event = pygame.event.Event(EventEnum.TRANSITION, transition=self.tmx_object)
        pygame.event.post(event)

    def draw(self, screen):
        pass

    def update(self, dt, *args):
        pass

