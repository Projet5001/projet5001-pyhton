# -*- coding: utf-8 -*-
#
# Projet5001: un jeu de survie post-apocalyptique
# Copyright (C) 2014  Équipe Projet5001
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import pygame

from eventManager import EventManager, EventEnum


class Keyboard():
    def __init__(self, game):
        self.game = game
        self.actor = game.perso
        self.speed = game.perso.speed
        self.accel = game.perso.accel
        self.coord_left = [-(self.speed * self.accel), 0]
        self.coord_right = [(self.speed * self.accel), 0]
        self.coord_up = [0, -(self.speed * self.accel)]
        self.coord_down = [0, (self.speed * self.accel)]

    def move_left(self):
        self.actor.move(self.coord_left[0], self.coord_left[1], "left")
        EventManager.envois_event(EventEnum.MOVE, 'left')

    def move_right(self):
        self.actor.move(self.coord_right[0], self.coord_right[1], "right")
        EventManager.envois_event(EventEnum.MOVE, "right")

    def move_up(self):
        self.actor.move(self.coord_up[0], self.coord_up[1], "up")
        EventManager.envois_event(EventEnum.MOVE, "up")

    def move_down(self):
        self.actor.move(self.coord_down[0], self.coord_down[1], "down")
        EventManager.envois_event(EventEnum.MOVE, "down")

    def jump(self):
        if self.actor.is_doing == "nothing":
            #self.actor.jump()
            #déclanche un event
            #pygame.time.set_timer(self.actor.actors_actions.event_jump, 40)#1 second is 1000 milliseconds
            EventManager.delay_event(EventEnum.JUMP, 40)

    def attack(self):
        if self.actor.is_doing == "nothing":
            EventManager.delay_event(EventEnum.ATTACK, 40)

    def pause_actor(self):
        self.actor.wait_frame()

    def block(self):
        self.actor.block()

    def show_player_hud(self):
        self.game.showHud("playerHud")
        self.game.addClockSec("playerHud", 1)

    def updateKey(self, dt):
        pressedkeys = pygame.key.get_pressed()
        self.actor.saveLastPos()

        if pressedkeys:
            if pressedkeys[pygame.K_LALT]:
                self.actor.active_arme(not self.actor.is_arme_active())

            if self.actor.is_doing == "nothing":

                if pressedkeys[pygame.K_LEFT]:
                    self.move_left()

                if pressedkeys[pygame.K_RIGHT]:
                    self.move_right()

                if pressedkeys[pygame.K_UP]:
                    self.move_up()

                if pressedkeys[pygame.K_DOWN]:
                    self.move_down()

                if pressedkeys[pygame.K_LCTRL]:
                    self.show_player_hud()

                if pressedkeys[pygame.K_SPACE]:
                    self.jump()
                elif pressedkeys[pygame.K_c]:
                    self.attack()

                self.est_imobile(pressedkeys)

    def est_imobile(self, pressedkeys):
        if not (pressedkeys[pygame.K_LEFT] or
                pressedkeys[pygame.K_RIGHT] or
                pressedkeys[pygame.K_UP] or
                pressedkeys[pygame.K_DOWN]):
                    self.actor.wait_frame()






