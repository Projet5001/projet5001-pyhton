#!env python
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

import os

import pygame
import monster

from lib import tmx

from gameconfig import GameConfig
from layermanager import LayerManager
from collisionManager import CollisionManager
from eventManager import EventManager
from stories.storymanager import StoryManager
import userInput
import playerHud
import player
from tools import weapon


class Game(object):

    def __init__(self, conffile):
        pygame.init()
        self.config = GameConfig(conffile)
        self.clock = pygame.time.Clock()

        self.layer_manager = LayerManager(self.config, self.clock)
        self.story_manager = StoryManager(self, self.layer_manager)
        self.collision_manager = CollisionManager(self.layer_manager)

        #list pour le joueur et monstre
        self.perso = None
        self.monstres = []

        self.layer_manager.set_map(self, self.config.get_start_map())
        self.layer_manager.new_layer('player', tmx.SpriteLayer)
        self.layer_manager.new_layer('npcs', tmx.SpriteLayer)
        self.layer_manager.new_layer('monster', tmx.SpriteLayer)

        self.FPS = 30
        self.clocks = {"playerHud": 0}
        self.userInput = None

    def start(self):
        #Trouve l'emplacement du héro
        source = self.layer_manager['boundaries'].find_source("start")

        self.layer_manager.set_focus(source.px, source.py, True)

        self.perso = self.charge_player()
        self.collision_manager.set_player(self.perso)
        self.perso.definir_position(source.px, source.py)

        self.monstres = self.charge_monstres()

        self.userInput = userInput.Keyboard(self)


        epe = weapon.Weapon(self.layer_manager, self.perso, 'clavier', 20, 50, 10)
        self.perso.ajoute_outils(epe, self.layer_manager)


        #hub
        self.createHuds()
        self.story_manager.read_stories(self.config.get_start_map())
        self.mainloop()

    def mainloop(self):
        while True:
            dt = self.clock.tick(self.FPS)

            quitter = EventManager.update(self)
            if quitter:
                return

            if not self.story_manager.blocking:
                self.userInput.updateKey(dt)

            for key, value in self.clocks.iteritems():
                if value >= 0:
                    if value == 0:
                        if key == "playerHud":
                            self.hideHud(key)
                            pass
                    else:
                        self.clocks[key] = value - 1

            #Récupère les collisions
            self.collision_manager.tmx_stackCollisionEvents()

            #stack les collision de monstre
            self.collision_manager.player_stackEvents()

            self.collision_manager.monster_stackEvents()

            #gère les évenement crée par le joureur
            self.collision_manager.player_manageCollisionEvents()

            #Gère les colisions selon leur nature
            self.collision_manager.tmx_manageCollisionEvents()

            self.collision_manager.monster_manageCollisionEvents()

            self.layer_manager.update(self.story_manager.blocking)
            self.layer_manager.draw()

            pygame.display.update()
            #pygame.display.flip()

    #factory pour monstre
    def charge_monstres(self):
        monstres = []

        try:
            for cell in self.layer_manager['pnjs'].find('monstre'):
                monster_layer = []
                if "visible" not in cell.properties or cell.properties['visible']:
                    monster_layer = self.layer_manager['monster']
                m = monster.Monster(cell.name,
                                    os.path.join(self.config.get_sprite_dir(),
                                                 "sprite-Ennemi.png"),
                                    (cell.px, cell.py), monster_layer)
                m.definir_position(cell.px, cell.py)
                monstres.append(m)
        except KeyError:
            pass

        return monstres

    def charge_player(self):
        return player.Player("player",
                             os.path.join(self.config.get_sprite_dir(),
                                          "sprite-Hero.png"),
                             (0, 0), self.layer_manager['player'])

    def do_trigger(self, trigger):
        self.story_manager.read_story(trigger)

    def effectuer_transition(self, limite):
        if not isinstance(limite, tmx.Object):
            pass

        try:
            if limite.properties['barree']:
                clef_requise = limite.properties['clef']
                if not clef_requise in self.perso.tools:
                    self.story_manager.display_speech([u"La porte est barrée... Il serait certainement possible de", u"l'ouvrir si tu avais une clé."], "top")
                    return
        except KeyError:
            # la porte n'est probablement pas barrée...
            pass

        self.deleteHuds()

        source_name = self.layer_manager.get_current_filename()
        if 'destination' in limite.properties:
            self.layer_manager.set_map(self, limite.properties['destination'])
            if 'dest_transition' in limite.properties:
                source = \
                    self.layer_manager['boundaries'].find_source(limite.properties['dest_transition'])
            else:
                source = \
                    self.layer_manager['boundaries'].find_source(source_name)
            self.createHuds()
            self.perso.definir_position(source.px, source.py)
            self.charge_monstres()
            self.layer_manager.set_focus(source.px, source.py, True)
            self.story_manager.read_stories(limite.properties['destination'])

    def createHuds(self):
        hud = playerHud.PlayerHud("playerHud",
                                  self.perso,
                                  self.layer_manager)
        self.layer_manager.add_layer(hud.name, hud)

    def showHud(self, name):
        layer = self.layer_manager[name]
        layer.setVisible(True)

    def hideHud(self, name):
        layer = self.layer_manager[name]
        layer.setVisible(False)

    def deleteHuds(self):
        if "playerHud" in self.layer_manager.layers:
            layer = self.layer_manager["playerHud"]
            self.layer_manager.remove(layer)
    def addClockSec(self, name, second):
        self.clocks[name] += second * self.FPS


if __name__ == '__main__':
    game = Game(os.path.join(os.path.dirname(__file__), "projet5001.json"))
    game.start()
