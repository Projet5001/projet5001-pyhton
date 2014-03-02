import pygame
import actors


class Player(actors.Actor):
    def __init__(self, image, position, *groups):
        super(Player, self).__init__(image, position, *groups)
        self.name = "Max Power"
        self.level = 99
        self.health = {"hp": 27, "max": 38}