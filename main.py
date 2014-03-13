# -*- coding: utf-8 -*-
import pygame
import monster
import os

from lib import tmx
import userInput
import playerHud
import player
import tools
import collisionManager
import actors_actions
from tools import weapon
rep_assets = os.path.join(os.path.dirname(__file__), "assets")
rep_sprites = os.path.join(rep_assets, "sprites")
rep_tilesets = os.path.join(rep_assets, "tilesets")


class Game(object):

    def __init__(self, start_map):
        self.screen = pygame.display.set_mode((640, 480))
        self.tilemap = tmx.load(os.path.join(rep_assets, start_map),
                                self.screen.get_size())
        self.clock = pygame.time.Clock()

        #list pour le joueur et monstre
        self.perso = None
        self.monstres = []

        #Créer un contenant pour les personnages et monstre
        self.player_layer = tmx.SpriteLayer()
        self.monster_layer = tmx.SpriteLayer()

        #Ajouter le personnage et monstres à la carte
        self.tilemap.layers.add_named(self.player_layer, 'player_layer')
        self.tilemap.layers.add_named(self.monster_layer, 'monster_layer')
        self.collision_manager = None
        self.FPS = 30
        self.clocks = {"playerHud": 0}
        self.userInput = None




    def start(self):
        #Trouve l'emplacement du héro
        source = self.tilemap.layers['boundaries'].find_source("start")

        self.tilemap.set_focus(source.px, source.py, True)

        self.perso = self.charge_player()
        self.perso.definir_position(source.px, source.py)
        self.monstres = self.charge_monstres()

        self.collision_manager = collisionManager.CollisionManager(self)
        self.userInput = userInput.Keyboard(self)



        #prototype !!!!!!!!!!
        #creation de l'arme
        epe = weapon.Weapon(self, self.perso, 'epe')

        #ajout de l'arme (je vais tenter de trouver un moyen de ne pas passé tilemap...)
        self.perso.ajoute_outils(epe)
        self.tilemap.layers.add_named(epe, 'epe')


        #prototype !!!!!!!!!!


        #hub
        self.createHuds()
        self.mainloop()

    def mainloop(self):
        while True:
            dt = self.clock.tick(self.FPS)
            # ces  5 lignes sont recquises pour passer les events
            # au gestionaire d'event de pygame
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_ESCAPE:
                    return
                if event.type == self.perso.actors_actions.event_jump:
                    print event
                    self.perso.actors_actions.update_frame_jump(event)

                if event.type == self.perso.actors_actions.event_attack:
                    print event
                    self.perso.actors_actions.update_frame_attack(event)

            # doit etre executé dans cette ordre

            self.userInput.updateKey(dt)

            for key, value in self.clocks.iteritems():
                if value >= 0:
                    if value == 0:
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

            self.tilemap.update(dt / 1000, self)

            self.screen.fill((0, 0, 0))

            self.tilemap.draw(self.screen)

            pygame.display.update()
            #pygame.display.flip()

    #factory pour monstre
    def charge_monstres(self):
        monstres = []

        try:
            for cell in self.tilemap.layers['pnjs'].find('monstre'):
                m = monster.Monster(os.path.join(rep_sprites, "sprite-Hero4.png"),
                                   (cell.px, cell.py), self.monster_layer)
                monstres.append(m)
        except KeyError:
            pass

        return monstres

    def charge_player(self):
        return player.Player(os.path.join(rep_sprites, "sprite-Hero4.png"),
                             (0, 0), self.player_layer)

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

        #recupere le groupe player
        players = self.tilemap.layers['player_layer']
        monstres = self.tilemap.layers['monster_layer']
        # future: equippement = self.tilemap.layers[self.perso.arme_equipe]
        equippement = self.tilemap.layers['epe']
        source_name = self.tilemap.filename
        if 'destination' in limite.properties:
            nouvelle_carte = \
                tmx.load(os.path.join(rep_assets,
                                      limite.properties['destination']),
                         self.screen.get_size())
            if nouvelle_carte:
                self.tilemap = nouvelle_carte
                self.collision_manager.set_tilemap(self.tilemap)
                source = \
                    self.tilemap.layers['boundaries'].find_source(source_name)
                self.tilemap.layers.add_named(players, 'player_layer')
                self.tilemap.layers.add_named(monstres, 'monster_layer')
                # future: self.tilemap.layers.add_named(equipement, self.perso.arme_equipe)
                self.tilemap.layers.add_named(equippement, 'epe')
                self.createHuds()
                self.perso.definir_position(source.px, source.py)
                self.charge_monstres()
                self.tilemap.set_focus(source.px, source.py, True)

    def createHuds(self):
        hud = playerHud.PlayerHud("playerHud",
                                  self.perso,
                                  self.screen,
                                  self.tilemap)
        self.tilemap.layers.add_named(hud, hud.name)

    def showHud(self, name):
        layer = self.tilemap.layers[name]
        layer.setVisible(True)

    def hideHud(self, name):
        layer = self.tilemap.layers[name]
        layer.setVisible(False)

    def deleteHuds(self):
        layer = self.tilemap.layers["playerHud"]
        self.tilemap.layers.remove(layer)

    def addClockSec(self, name, second):
        self.clocks[name] += second * self.FPS


if __name__ == '__main__':
    pygame.init()
    game = Game("ageei.tmx")  # TODO: lire d'un fichier de config
    game.start()
