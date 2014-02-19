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
        self.tilemap = tmx.load(os.path.join(rep_assets, "ageei.tmx"), screen.get_size())

        self.clock = pygame.time.Clock()

        #creatre container for all player
        self.players = tmx.SpriteLayer()

        #you can read ?  ;)
        self.stackEvents = []

        #find player start position, fot now this in only as an example
        start_cell = self.tilemap.layers['pnjs'].find('player')[0]

        self.perso = actors.Actor(os.path.join(rep_sprites, "perso.png"), (start_cell.px, start_cell.py), self.players)

        self.userInput = userInput.Keyboard(self.perso)

        #add players container to tilemap
        self.tilemap.layers.append(self.players)

        while True:
            dt = self.clock.tick(30)
            #ces  5 lignes sont recquises pour passer les events au gestionaire d'event de pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            # doit etre executer dans cette ordre
            self.userInput.updateKey(dt)

            #manage collision events
            self.stackCollisionEvents(self.perso, self.stackEvents)
            #this litle one here act as a man in the middle or negotiator
            self.manageCollisionEvents(self.perso, self.tilemap, self.stackEvents)

            #dont move
            self.tilemap.update(dt, self)

            #dont move
            screen.fill((0,0,0))

            #dont move
            self.tilemap.draw(screen)

            #dont move
            #ugly need to find a way to call this an other way
            pygame.display.flip()


    # system un peu plus pres du MVC qui stack tous les event du monde
    def stackCollisionEvents(self, perso, stackEvents):
        pass
        #vérifie si il y a collision entre rect et un objet qui a a la propriété block
        # retourne un rect
        for cell in self.tilemap.layers['boundaries'].collide(perso.collision_rect,'boundary'):
            stackEvents.append(cell)
        for cell in self.tilemap.layers['walls'].collide(perso.collision_rect,'wall'):
            stackEvents.append(cell)

    # systeme qui pop les event et les gere  (cest un médiateur entre acteur tilemap)
    def manageCollisionEvents(self, perso, tilemap, stackEvents):
        while len(stackEvents) > 0:
            e = stackEvents.pop()

            try:
                if e['block']:
                    print "event"
                    if perso.isDoing == "noBlock":
                        pass
                    else:
                        perso.resetPos()
            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas mettre
                # de propriété à la cellule... :(
                perso.resetPos()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
