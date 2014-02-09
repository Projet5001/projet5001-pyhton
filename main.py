# -*- coding: utf-8 -*-
import pygame
import tmx
import cfg
import actors
import userInput


class Game(object):

    def main(self, screen):
        self.tilemap = tmx.load('example.tmx', screen.get_size())
        self.config = cfg.Config(self.tilemap, screen)
        self.clock = pygame.time.Clock()
        self.players = tmx.SpriteLayer()


        start_cell = self.tilemap.layers['objet'].find('player')[0]
        print start_cell


        self.perso = actors.Actor(screen, "perso.png", (start_cell.px, start_cell.py), self.players)
        self.userInput = userInput.Keyboard(self.config, self.perso)
        self.tilemap.layers.append(self.players)


        while True:
            dt = self.clock.tick(30)

            self.userInput.updateKey()

            #ces  5 lignes sont recquises pour passer les events au gestionaire d'event de pygame
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return


            self.tilemap.update(dt, self)
            screen.fill((0,0,0))

            self.tilemap.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
