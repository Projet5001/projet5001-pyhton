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

    #overide
    def spritecollideany(self, collided = None):
        try:
            for tool in self.player.tools.values():
                sprite = tool

                if collided is None:
                    for s in self.layer_manager['monster']:
                        if self.player.is_arme_active() and sprite.rect.colliderect(s.rect):
                            return s
                else:
                    for s in self.layer_manager['monster']:
                        if collided(sprite, s):
                            return s
        except KeyError:
            pass

        return None

    def player_stackEvents(self):

        coll = self.spritecollideany()
        if coll:
            print 'collision'
            self.player_events.append(coll)

        for s in self.layer_manager['npcs']:
            if self.player.collision_rect.colliderect(s.collision_rect):
                self.player_events.append(s)

    def player_manageCollisionEvents(self):

        while len(self.player_events) > 0:
            e = self.player_events.pop()

            #TODO: reset position...
            if e.block and e.attack:
                e.take_dommage(self.player.calcul_dommage())
                print e.health['hp']

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
