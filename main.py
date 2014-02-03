# -*- coding: utf-8 -*-
import pygame
import tmx
from userInput import *
from perso import *
from config import *


def main():
    pygame.init()
    screensize = (640, 480)
    screen = pygame.display.set_mode(screensize)
    tilemap = tmx.load('example.tmx', screen.get_size())
    tilemap.set_focus(0, 0)
    config = Config(tilemap, screen)
    clock = pygame.time.Clock()
    dt = clock.tick(30)
    perso = Perso(screen, "perso.png")
    userInput = UserInput(config, perso, tilemap)


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        tilemap.update(dt)
        black = (0,0,0)
        screen.fill(black)
        # Draw all layers of the tilemap to the screen.
        tilemap.draw(screen)
        userInput.update()
        perso.update()
        # Refresh the display window.
        pygame.display.flip()



if __name__ == '__main__':
    main()