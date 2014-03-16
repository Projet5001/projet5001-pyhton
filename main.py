# -*- coding: utf-8 -*-
import pygame
import monster
import os

from lib import tmx
import userInput
import playerHud
import player
import tools
import actors_actions
from tools import weapon
from gameconfig import GameConfig
from layermanager import LayerManager
from collisionManager import CollisionManager


class Game(object):

    def __init__(self, conffile):
        pygame.init()
        self.config = GameConfig(conffile)
        self.clock = pygame.time.Clock()

        self.layer_manager = LayerManager(self.config, self.clock)
        self.collision_manager = CollisionManager(self, self.layer_manager)

        #list pour le joueur et monstre
        self.perso = None
        self.monstres = []

        self.layer_manager.set_map(self, self.config.get_start_map())
        self.layer_manager.new_layer('player', tmx.SpriteLayer)
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

        #prototype !!!!!!!!!!
        #creation de l'arme
        epe = weapon.Weapon(self.layer_manager, self.perso, 'epe')

        #ajout de l'arme (je vais tenter de trouver un moyen de ne pas passé tilemap...)
        self.perso.ajoute_outils(epe, self.layer_manager)
        #prototype !!!!!!!!!!

        #hub
        self.createHuds()
        self.mainloop()

    def mainloop(self):
        while True:
            dt = self.clock.tick(self.FPS)
            # ces lignes sont recquises pour passer les events
            # au gestionaire d'event de pygame
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    return

                if event.type == self.perso.actors_actions.event_jump:
                    self.perso.actors_actions.update_frame_jump(event)

                if event.type == self.perso.actors_actions.event_attack:
                    self.perso.actors_actions.update_frame_attack(event)

                if event.type == pygame.USEREVENT+3:
                    self.effectuer_transition(event.transition)

            # doit etre executé dans cette ordre
            self.userInput.updateKey(dt)

            for key, value in self.clocks.iteritems():
                if value >= 0:
                    if value == 0:
                        if key == "playerHud":
                            self.hideHud(key)
                    else:
                        self.clocks[key] = value - 1

            #Récupère les collisions
            self.collision_manager.tmx_stackCollisionEvents()

            #stack les collision de monstre
            self.collision_manager.player_stackEvents()

            #gère les évenement crée par le joureur
            self.collision_manager.player_manageCollisionEvents()

            #Gère les colisions selon leur nature
            self.collision_manager.tmx_manageCollisionEvents()

            self.layer_manager.update()
            self.layer_manager.draw()

            pygame.display.update()
            #pygame.display.flip()

    #factory pour monstre
    def charge_monstres(self):
        monstres = []

        try:
            for cell in self.layer_manager['pnjs'].find('monstre'):
                m = monster.Monster(os.path.join(self.config.get_sprite_dir(),
                                                 "sprite-Hero4.png"),
                                   (cell.px, cell.py), self.layer_manager['monster'])
                monstres.append(m)
        except KeyError:
            pass

        return monstres

    def charge_player(self):
        return player.Player(os.path.join(self.config.get_sprite_dir(),
                                          "sprite-Hero4.png"),
                             (0, 0), self.layer_manager['player'])

    def effectuer_transition(self, limite):
        if not isinstance(limite, tmx.Object):
            pass

        try:
            if limite.properties['barree']:
                clef_requise = limite.properties['clef']
                if not clef_requise in self.perso.tools:
                    return
        except KeyError:
            # la porte n'est probablement pas barrée...
            pass

        self.deleteHuds()

        source_name = self.layer_manager.get_current_filename()
        if 'destination' in limite.properties:
            self.layer_manager.set_map(self, limite.properties['destination'])
            source = \
                self.layer_manager['boundaries'].find_source(source_name)
            self.createHuds()
            self.perso.definir_position(source.px, source.py)
            self.charge_monstres()
            self.layer_manager.set_focus(source.px, source.py, True)

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
