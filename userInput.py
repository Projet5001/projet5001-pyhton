# -*-coding:utf-8-*-


import pygame


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

    def move_right(self):
        self.actor.move(self.coord_right[0], self.coord_right[1], "right")

    def move_up(self):
        self.actor.move(self.coord_up[0],self.coord_up[1], "up")

    def move_down(self):
        self.actor.move(self.coord_down[0],self.coord_down[1], "down")

    def jump(self):
        pygame.time.set_timer(self.game.persoJump, 150)#1 second is 1000 milliseconds

    def attack(self):
        pygame.time.set_timer(self.game.persoAttack, 150)#1 second is 1000 milliseconds



    def block(self):
        self.actor.block()

    def show_player_hud(self):
        self.game.showHud("playerHud")
        self.game.addClockSec("playerHud", 1)

    def updateKey(self, dt, desactiv_commande):
        pressedkeys = pygame.key.get_pressed()
        self.actor.saveLastPos()

        if pressedkeys[pygame.K_LALT]:
            self.actor.active_arme(not self.actor.is_arme_active())

        if desactiv_commande  == 1:
            pass
        else:
            if pressedkeys[pygame.K_LEFT]:
                self.move_left()

            if pressedkeys[pygame.K_RIGHT]:
                self.move_right()

            if pressedkeys[pygame.K_UP]:
                self.move_up()

            if pressedkeys[pygame.K_DOWN]:
                self.move_down()

            if pressedkeys[pygame.K_SPACE]:
                self.jump()

            if pressedkeys[pygame.K_LCTRL]:
                self.show_player_hud()

            if pressedkeys[pygame.K_c]:
                self.attack()


