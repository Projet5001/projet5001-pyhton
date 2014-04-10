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
from pygame import rect as rect

import chargerImagesSprite
import actors_actions


class Actor(pygame.sprite.Sprite):
    def __init__(self, name, image, nombre_lignes, position, *groups):
        super(Actor, self).__init__(*groups)
        # self.image = pygame.image.load(image)
        self.name = name
        self.charger_Images_Sprite = chargerImagesSprite.Charger_Images_Sprite(image, nombre_lignes)

        self.personnage = self.charger_Images_Sprite.personnage
        self.image = self.personnage[4]

        self.rect = pygame.rect.Rect(position, self.image.get_size())
        self.collision_rect = pygame.rect.Rect(position[0] - 20,
                                               position[1] - 100,
                                               40,
                                               30)

        self.actors_actions = actors_actions.ActorActions(self.image, self.personnage, self)
        self.tools = {}
        self.saveLastPos()

        self.coord_to_move = {"posX":0, "posY":0 ,"side":"none"}

        #encoure utile ???
        self.cycle_est_fini = False
        self.compteur_cycle = 0
        self.horloge = 0
        self.a_fini_cycle = 0
        self.compteur = 0
        self.wait_actors = False

        #isetheral
        self.not_ehteral = True

        #spec of perso
        self.dommage = 1
        self.protection = 0
        self.speed = 8
        self.accel = 1
        self.is_doing = "nothing"
        self.arme_equipe = ""
        self.level = 0
        self.health = {"hp": 0, "max": 0}

    def save_x_pos(self):
        self.last_x = self.rect.x
        self.last_coll_x = self.collision_rect.x

    def save_y_pos(self):
        self.last_y = self.rect.y
        self.last_coll_y = self.collision_rect.y

    def saveLastPos(self):
        self.save_x_pos()
        self.save_y_pos()

    def resetX(self):
        self.rect.x = self.last_x
        self.collision_rect.x = self.last_coll_x
        self.save_x_pos()

    def resetY(self):
        self.rect.y = self.last_y
        self.collision_rect.y = self.last_coll_y
        self.save_y_pos()

    def resetPos(self):
        self.resetX()
        self.resetY()

    def definir_position(self, x, y):
        self.rect.x = x - 40
        self.rect.y = y - 75
        self.collision_rect.x = x
        self.collision_rect.y = y
        self.saveLastPos()


    def move(self, x, y,laDirection, define_frame = "none"):
        #print "dans la class Actor la direction recu ===  "+str(laDirection)
        self.coord_to_move["posX"] = x
        self.coord_to_move["posY"] = y
        self.coord_to_move["side"] = laDirection
        self.coord_to_move["define_frame"] = define_frame

        self.image =  self.actors_actions.mouvement(self.coord_to_move)
        self.rect.move_ip(x, y)
        self.collision_rect.move_ip(x, y)
        for tool in self.tools.values():
            tool.definir_position(self.rect.x, self.rect.y)

    def jump(self, tell_frame):
        self.actors_actions.action("jump", tell_frame)
        self.image = self.actors_actions.image

    def attack(self, tell_frame):
        self.actors_actions.action("attack", tell_frame)
        self.image = self.actors_actions.image

    def wait_frame(self):
        self.actors_actions.frame_pause()
        self.image = self.actors_actions.image

    def calcul_dommage(self):
        return self.dommage * self.luck() * self.get_tool().dommage


    def active_arme(self, active):
        self.tools[self.arme_equipe].visible = active

    def get_tool(self):
        if self.arme_equipe != "":
            return self.tools[self.arme_equipe]
        else:
            return self

    def is_arme_active(self):
        return self.tools[self.arme_equipe].visible

    def take_dommage(self, dommage):
        self.health['hp'] -= (dommage - self.protectionTotal())
        self.isBleeding()
        print self.health['hp']

    def block(self):
        return

    def luck(self):
        return 1

    def protectionTotal(self):
        return self.protection

    def ajoute_outils(self, tool, tilemap):
        self.tools[tool.name] = tool
        tool.definir_position(self.rect.x, self.rect.y)
        tilemap.add_layer(type(tool).__name__, tool)
        if type(tool).__name__ == 'Weapon':
            self.arme_equipe = tool.name

    def isBleeding(self):
        if self.health['hp'] <= 0:
            self.kill()

    # this need the dt and game otherwise bug in tmx
    def update(self, dt, game):
        pass
