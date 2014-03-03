# -*- coding: utf-8 -*-

import actors
import tools

class Player(actors.Actor):
    def __init__(self, image, position, *groups):
        super(Player, self).__init__(image, position, *groups)
        self.speed = 10

        #pour les test du HUD
        self.name = "Max Power"
        self.level = 99
        self.health = {"hp": 27, "max": 38}

    def block(self):
        self.protection = 1
        print "protection"

    def update(self, dt, game):
        game.tilemap.set_focus(self.collision_rect.x, self.collision_rect.y)
        self.protection = 0
