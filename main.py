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



    def main(self, screen):
        self.tilemap = tmx.load(os.path.join(rep_assets, "ageei.tmx"),
                                screen.get_size())
        self.clock = pygame.time.Clock()
        self.screen = screen
        #Créer un contenant pour les personnages et monstre
        self.players = tmx.SpriteLayer()
        self.monsters = tmx.SpriteLayer()
        self.tmxEvents = []
        self.playerEvents = []

        #Trouve l'emplacement des acteur

        self.perso = self.charge_player()
        self.charge_monstre()
        self.userInput = userInput.Keyboard(self.perso)

        #Ajouter le personnage à la carte

        self.tilemap.layers.append(self.players)
        self.tilemap.layers.append(self.monsters)
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
            self.player_stackEvents(self.perso, self.monsters, self.playerEvents)

            #gère les évenement crée par le joureur
            self.player_manageCollisionEvents(self.perso, self.playerEvents)

            #Gère les colisions selon leur nature
            self.tmx_manageCollisionEvents(self.perso, self.tmxEvents)

            self.tilemap.update(dt/1000., self)

            self.tilemap.draw(screen)

            pygame.display.update()

    def charge_monstre(self):
        for cell in self.tilemap.layers['pnjs'].find('monstre'):
            monster.Monster(os.path.join(rep_sprites, "perso.png"), (cell.px, cell.py), self.monsters)

    def charge_player(self):
        start_cell = self.tilemap.layers['pnjs'].find('player')[0]
        return player.Player(os.path.join(rep_sprites, "perso.png"),
                             (start_cell.px, start_cell.py),
                             self.players)

    # system un peu plus pres du MVC qui stack tous les event du monde
    def tmx_stackCollisionEvents(self, perso, tmxEvents):
        pass
        #vérifie si il y a collision entre rect et un objet qui a a la
        # propriété block retourne un rect
        layers = self.tilemap.layers

        for cell in layers['boundaries'].collide(perso.collision_rect, 'boundary'):
            tmxEvents.append(cell)
        for cell in layers['walls'].collide(perso.collision_rect, 'wall'):
            tmxEvents.append(cell)


    # systeme qui pop les event et les gere
    # (cest un médiateur entre acteur tilemap)
    def tmx_manageCollisionEvents(self, perso, tmxEvents):
        while len(tmxEvents) > 0:
            e = tmxEvents.pop()

            try:
                if e['wall'] or e['boundary']:
                    perso.resetPos()

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                perso.resetPos()

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
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
