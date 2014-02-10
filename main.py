# -*- coding: utf-8 -*-
import pygame
import tmx
import cfg
import actors
import userInput


class Game(object):

    def main(self, screen):
        self.tilemap = tmx.load('example.tmx', screen.get_size())

        #still in use ?
        self.config = cfg.Config(self.tilemap, screen)

        self.clock = pygame.time.Clock()

        #creatre container for all player
        self.players = tmx.SpriteLayer()

        #you can read ?  ;)
        self.stackEvents = []

        #find player start position, fot now this in only as an example
        start_cell = self.tilemap.layers['objet'].find('player')[0]

        self.perso = actors.Actor("perso.png", (start_cell.px, start_cell.py), self.players)

        self.userInput = userInput.Keyboard(self.config, self.perso)

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

        #vérifie si il y a collision entre rect et un objet qui a a la propriété block
        # retourne un rect
        for cell in self.tilemap.layers['objet'].collide(perso.rect,'block'):
            stackEvents.append(cell)

    # systeme qui pop les event et les gere  (cest un médiateur entre acteur tilemap)
    def manageCollisionEvents(self, perso, tilemap, stackEvents):
        while len(stackEvents) > 0:
            e = stackEvents.pop()

            if e['block']:
                print "event"
                if perso.isDoing == "noBlock":
                    pass
                else:
                    perso.resetPos()



if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
