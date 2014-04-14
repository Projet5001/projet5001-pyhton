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
from eventManager import EventEnum, EventManager
from lib import tmx

from tools.basetool import BaseTool


class CollisionManager():

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager
        self.player = None
        self.player_events = []
        self.tmx_events = []

        self.object_reference = {}

    def set_player(self, player):
        self.player = player

    def player_stackEvents(self):

        for s in self.layer_manager['monster']:
            if self.player.collision_rect.colliderect(s.collision_rect):
                self.player_events.append(s)
            elif self.player.get_tool().rect.colliderect(s.rect) and self.player.is_doing == "attack":
                print "attack  and dommage"
                s.take_dommage(self.player.calcul_dommage())
        for s in self.layer_manager['npcs']:
            if self.player.collision_rect.colliderect(s.collision_rect):
                self.player_events.append(s)



    def player_manageCollisionEvents(self):

        while len(self.player_events) > 0:
            e = self.player_events.pop()
            if e.not_ehteral:
                self.player.resetPos()

    def monster_stackEvents(self):

        boundaries = self.layer_manager['boundaries']
        walls = self.layer_manager['walls']

        for monstre in self.layer_manager['monster']:
            for cell in walls.collideLayer(monstre.collision_rect):
                monstre.collision_events.append(cell)
            for objet in boundaries.collide(monstre.collision_rect, 'block'):
                monstre.collision_events.append(objet)
            for s in self.layer_manager['npcs']:
                if monstre.collision_rect.colliderect(s.collision_rect):
                    monstre.collision_events.append(s)
            if monstre.collision_rect.colliderect(self.player.collision_rect):
                monstre.resetPos()
                self.player.take_dommage(s.calcul_dommage())
                
    def monster_manageCollisionEvents(self):

        for monstre in self.layer_manager['monster']:
            while len(monstre.collision_events) > 0:
                e = monstre.collision_events.pop()
                axis = self.evaluate_collision_axis(e, monstre)
                if axis == "xy":
                    monstre.resetPos()
                elif axis == "x":
                    monstre.resetX()
                elif axis == "y":
                    monstre.resetY()

    def tmx_stackCollisionEvents(self):

        boundaries = self.layer_manager['boundaries']
        walls = self.layer_manager['walls']
        objets = None
        try:
            objets = self.layer_manager['objets']
        except KeyError:
            pass

        for cell in walls.collideLayer(self.player.collision_rect):
            self.tmx_events.append(cell)

        for objet in boundaries.collide(self.player.collision_rect, 'block'):
            self.tmx_events.append(objet)

        for objet in boundaries.collide(self.player.collision_rect, 'basetool'):
            tool = None
            if objet not in self.object_reference:
                self.object_reference[objet] = \
                    BaseTool.make_tool(self.layer_manager, self.player, objet)
            else:
                tool = self.object_reference[objet]

            if tool:
                self.tmx_events.append(tool)

        if objets:
            for objet in objets.collide_any(self.player.collision_rect):
                tool = None

                if objet not in self.object_reference:
                    self.object_reference[objet] = \
                        BaseTool.make_tool(self.layer_manager, self.player, objet)
                else:
                    tool = self.object_reference[objet]

                if tool:
                    self.tmx_events.append(tool)

    def evaluate_collision_axis(self, e, sprite):
        ''' Essaye de trouver en quel axe on est bloqués, question de pouvoir
            continuer le mouvement dans l'autre axe. '''

        axes = ""
        sprite_rect = sprite.collision_rect
        e_rect = pygame.Rect(e.left, e.top, e.width, e.height)

        top = (
             e_rect.collidepoint(sprite_rect.topleft),
             e_rect.collidepoint(sprite_rect.midtop),
             e_rect.collidepoint(sprite_rect.topright),
        )
        right = (
             e_rect.collidepoint(sprite_rect.topright),
             e_rect.collidepoint(sprite_rect.midright),
             e_rect.collidepoint(sprite_rect.bottomright),
        )
        left = (
             e_rect.collidepoint(sprite_rect.topleft),
             e_rect.collidepoint(sprite_rect.midleft),
             e_rect.collidepoint(sprite_rect.bottomleft),
        )
        bottom = (
             e_rect.collidepoint(sprite_rect.bottomleft),
             e_rect.collidepoint(sprite_rect.midbottom),
             e_rect.collidepoint(sprite_rect.bottomright),
        )

        #print "--------"
        #print "top %s" % top.__str__()
        #print "right %s" % right.__str__()
        #print "left %s" % left.__str__()
        #print "bottom %s" % bottom.__str__()

        if sum(v for v in left) >= 2 or sum(v for v in right) >= 2:
            axes = axes + "x"
        if sum(v for v in top) >= 2 or sum(v for v in bottom) >= 2:
            axes = axes + "y"

        return axes

    def tmx_manageCollisionEvents(self):

        while len(self.tmx_events) > 0:
            e = self.tmx_events.pop()

            if isinstance(e, tmx.Cell) or isinstance(e, tmx.Object):
                axis = self.evaluate_collision_axis(e, self.player)
                if axis == "xy":
                    self.player.resetPos()
                elif axis == "x":
                    self.player.resetX()
                elif axis == "y":
                    self.player.resetY()
            elif isinstance(e, BaseTool):
                e.handle_collision()
