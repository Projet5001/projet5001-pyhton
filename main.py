# -*- coding: utf-8 -*-
import pygame

import os
import actors
from lib import tmx
import userInput
import playerHud
import player

rep_assets = os.path.relpath("assets")
rep_sprites = os.path.join(rep_assets, "sprites")
rep_tilesets = os.path.join(rep_assets, "tilesets")


class Game(object):

    def __init__(self, start_map):
        self.screen = pygame.display.set_mode((640, 480))
        self.tilemap = tmx.load(os.path.join(rep_assets, start_map),
                                self.screen.get_size())
        self.clock = pygame.time.Clock()
        #Créer un contenant pour les personnages
        self.players = tmx.SpriteLayer()
        self.stackEvents = []

        self.perso = player.Player(os.path.join(rep_sprites, "perso.png"),
                                  (0, 0), self.players)

        self.FPS = 30
        self.clocks = {"playerHud": 0}

    def start(self):
        #Trouve l'emplacement du héro
        source = \
            self.tilemap.layers['boundaries'].find_source("start")
        self.tilemap.set_focus(source.px, source.py, True)
        self.perso.definir_position(source.px, source.py)
        self.userInput = userInput.Keyboard(self)
        #Ajouter le personnage à la carte
        self.tilemap.layers.append(self.players)
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

            # doit etre executé dans cette ordre
            self.userInput.updateKey(dt)

            for key, value in self.clocks.iteritems():
                if (value >= 0):
                    if(value == 0):
                        self.hideHud(key)
                    else:
                        self.clocks[key] = value - 1

            #Récupère les collisions
            self.stackCollisionEvents(self.perso, self.stackEvents)
            #Gère les colisions selon leur nature
            self.manageCollisionEvents(self.perso,
                                       self.tilemap,
                                       self.stackEvents)

            self.tilemap.update(dt, self)
            self.screen.fill((0, 0, 0))
            self.tilemap.draw(self.screen)
            #TODO: trouver un façon d'appeller cette méthode
            pygame.display.flip()

    # system un peu plus pres du MVC qui stack tous les event du monde
    def stackCollisionEvents(self, perso, stackEvents):
        #vérifie si il y a collision entre rect et un objet qui a a la
        # propriété block retourne un rect
        boundaries = self.tilemap.layers['boundaries']
        walls = self.tilemap.layers['walls']
        for cell in walls.collideLayer(perso.collision_rect):
            stackEvents.append(cell)
        for cell in boundaries.collide(perso.collision_rect, 'block'):
            stackEvents.append(cell)

    # systeme qui pop les event et les gere
    # (cest un médiateur entre acteur tilemap)
    def manageCollisionEvents(self, perso, tilemap, stackEvents):
        while len(stackEvents) > 0:
            e = stackEvents.pop()

            try:
                if isinstance(e, tmx.Cell):
                    perso.resetPos()
                elif len(stackEvents) == 0 and isinstance(e, tmx.Object):
                    perso.resetPos()
                    self.effectuer_transition(e)
            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                perso.resetPos()

    def effectuer_transition(self, limite):
        if not isinstance(limite, tmx.Object):
            pass

        self.deleteHuds()
        players = self.tilemap.layers.pop()
        source_name = self.tilemap.filename
        if 'destination' in limite.properties:
            nouvelle_carte = \
                tmx.load(os.path.join(rep_assets,
                                      limite.properties['destination']),
                         self.screen.get_size())
            if nouvelle_carte:
                self.tilemap = nouvelle_carte
                source = \
                    self.tilemap.layers['boundaries'].find_source(source_name)
                self.tilemap.layers.append(players)
                self.perso.definir_position(source.px, source.py)
                self.tilemap.set_focus(source.px, source.py, True)
                self.createHuds()

    def createHuds(self):
        hud = playerHud.PlayerHud("playerHud", self.perso, self)
        self.tilemap.layers.add_named(hud, hud.name)

    def showHud(self, name):
        layer = self.tilemap.layers.__getitem__(name)
        layer.setVisible(True)

    def hideHud(self, name):
        layer = self.tilemap.layers.__getitem__(name)
        layer.setVisible(False)

    def deleteHuds(self):
        layer = self.tilemap.layers.__getitem__("playerHud")
        self.tilemap.layers.remove(layer)

    def addClockSec(self, name, second):
        self.clocks[name] += second * self.FPS

gi 
if __name__ == '__main__':
    pygame.init()
    game = Game("ageei.tmx") #TODO: lire d'un fichier de config
    game.start()