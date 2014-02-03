# -*- coding: utf-8 -*-
import pygame
import tmx
from userInput import *
from perso import *
from config import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

if __name__ == '__main__':
    main()