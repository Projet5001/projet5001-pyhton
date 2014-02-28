# -*- coding: utf-8 -*-
import pygame
from pygame import sprite as p_sprt
import monster
import os
import player
from lib import tmx
import userInput

rep_assets = os.path.relpath("assets")
rep_sprites = os.path.join(rep_assets, "sprites")
rep_tilesets = os.path.join(rep_assets, "tilesets")


class Game(object):

    def __init__(self, start_map):
        self.screen = pygame.display.set_mode((640, 480))
        self.tilemap = tmx.load(os.path.join(rep_assets, start_map),
                                self.screen.get_size())
        self.clock = pygame.time.Clock()
        self.tmxEvents = []
        self.playerEvents = []

        #Créer un contenant pour les personnages et monstre
        self.player_layer = tmx.SpriteLayer()
        self.monster_layer = tmx.SpriteLayer()

        #Ajouter le personnage et monstres à la carte
        self.tilemap.layers.append(self.player_layer)
        self.tilemap.layers.append(self.monster_layer)

    def start(self):
        #Trouve l'emplacement du héro
        source = \
            self.tilemap.layers['boundaries'].find_source("start")
        self.tilemap.set_focus(source.px, source.py, True)

        self.perso = self.charge_player()
        self.perso.definir_position(source.px, source.py)

        self.monstres = self.charge_monstres()

        self.userInput = userInput.Keyboard(self)

        self.mainloop()

    def mainloop(self):
        while True:
            dt = self.clock.tick(30)
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

            #Récupère les collisions
            self.tmx_stackCollisionEvents(self.perso, self.tmxEvents)

            #stack les collision de monstre
            self.player_stackEvents(self.perso, self.monster_layer, self.playerEvents)

            #gère les évenement crée par le joureur
            self.player_manageCollisionEvents(self.perso, self.playerEvents)

            #Gère les colisions selon leur nature
            self.tmx_manageCollisionEvents(self.perso, self.tmxEvents)

            self.tilemap.update(dt/1000, self)

            self.screen.fill((0, 0, 0))
            self.tilemap.draw(self.screen)

            pygame.display.update()
            #pygame.display.flip()

    def charge_monstres(self):
	monstres = []
        for cell in self.tilemap.layers['pnjs'].find('monstre'):
            monstre = monster.Monster(os.path.join(rep_sprites, "perso.png"),
                                      (cell.px, cell.py), self.monster_layer)
            monstres.append(monstre)
        return monstres

    def charge_player(self):
        return player.Player(os.path.join(rep_sprites, "perso.png"),
                             (0, 0), self.player_layer)

    def tmx_stackCollisionEvents(self, perso, tmxEvents):
        boundaries = self.tilemap.layers['boundaries']
        walls = self.tilemap.layers['walls']
        for cell in walls.collideLayer(perso.collision_rect):
            tmxEvents.append(cell)
        for cell in boundaries.collide(perso.collision_rect, 'block'):
            tmxEvents.append(cell)

    # systeme qui pop les event et les gere
    # (cest un médiateur entre acteur tilemap)
    def tmx_manageCollisionEvents(self, perso, tmxEvents):
        while len(tmxEvents) > 0:
            e = tmxEvents.pop()

            try:
                if isinstance(e, tmx.Cell):
                    perso.resetPos()
                elif len(tmxEvents) == 0 and isinstance(e, tmx.Object):
                    perso.resetPos()
                    self.effectuer_transition(e)

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                perso.resetPos()

    def effectuer_transition(self, limite):
        if not isinstance(limite, tmx.Object):
            pass

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
                self.monstres = self.charge_monstres()
                self.tilemap.set_focus(source.px, source.py, True)

    def show_hud(self):
        print self.perso.collision_rect

    def player_stackEvents(self, sprit, groupe, playerEvents):

        coll = p_sprt.spritecollideany(sprit, groupe)
        if coll:
         print coll
         playerEvents.append(coll)

    def player_manageCollisionEvents(self,player, playerEvents):
        while len(playerEvents) > 0:
            e = playerEvents.pop()
            if e.block and e.attack:
                player.take_dommage(e.attack())
                print player.life

if __name__ == '__main__':
    pygame.init()
    game = Game("ageei.tmx") #TODO: lire d'un fichier de config
    game.start()
