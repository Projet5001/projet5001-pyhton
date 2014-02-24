# -*- coding: utf-8 -*-
import pygame

import os
import actors
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
        #Créer un contenant pour les personnages
        self.players = tmx.SpriteLayer()
        self.stackEvents = []
        #Trouve l'emplacement du héro
        start_cell = self.tilemap.layers['pnjs'].find('player')[0]
        self.perso = actors.Actor(os.path.join(rep_sprites, "perso.png"),
                                  (start_cell.px, start_cell.py),
                                  self.players)
        self.userInput = userInput.Keyboard(self.perso)
        #Ajouter le personnage à la carte
        self.tilemap.layers.append(self.players)

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
            self.stackCollisionEvents(self.perso, self.stackEvents)
            #Gère les colisions selon leur nature
            self.manageCollisionEvents(self.perso,
                                       self.tilemap,
                                       self.stackEvents)

            self.tilemap.update(dt, self)
            screen.fill((0, 0, 0))
            self.tilemap.draw(screen)
            #TODO: trouver un façon d'appeller cette méthode
            pygame.display.flip()

    # system un peu plus pres du MVC qui stack tous les event du monde
    def stackCollisionEvents(self, perso, stackEvents):
        pass
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
                if e['wall'] or e['boundary']:
                    perso.resetPos()
            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                perso.resetPos()

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
