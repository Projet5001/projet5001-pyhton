# -*- coding: utf-8 -*-
import pygame
import tmx

class UserInput:
    def __init__(self, perso):
        self.perso = perso

    def update(self):
       pass

class Perso(pygame.sprite.Sprite):
    def __init__(self, screen, image):
        super(Perso, self).__init__()
        pass


    def update(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()


if __name__ == '__main__':
    main()