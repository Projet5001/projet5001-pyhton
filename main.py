# -*- coding: utf-8 -*-
import pygame
import tmx
import cfg
import actors
import userInput


class Game(object):

    def main(self,screen):
        self.tilemap = tmx.load('example.tmx', screen.get_size())
        self.config = cfg.Config(self.tilemap, screen)
        self.clock = pygame.time.Clock()
        self.players = tmx.SpriteLayer()
        self.perso = actors.Actor(screen, "perso.png", self.players)
        self.userInput = userInput.Keyboard(self.config, self.perso, self.tilemap)
        self.tilemap.layers.append(self.players)
        # add an enemy for each "enemy" trigger in the map

        while True:
            dt = self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            self.tilemap.update(dt, self)
            screen.fill((0,0,0))

            self.tilemap.draw(screen)
            pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    Game().main(screen)
