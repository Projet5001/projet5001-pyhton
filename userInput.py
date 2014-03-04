import pygame


class Keyboard():
    def __init__(self, game):
        self.game = game
        self.actor = game.perso
        self.speed = game.perso.speed
        self.accel = game.perso.accel

    def move_left(self):
        self.actor.move(-(self.speed * self.accel), 0)

    def move_right(self):
        self.actor.move((self.speed * self.accel), 0)

    def move_up(self):
        self.actor.move(0, -(self.speed * self.accel))

    def move_down(self):
        self.actor.move(0, (self.speed * self.accel))

    def jump(self):
        pass

    def block(self):
        self.actor.block()

    def show_player_hud(self):
        self.game.showHud("playerHud")
        self.game.addClockSec("playerHud", 1)

    def updateKey(self, dt):
        pressedkeys = pygame.key.get_pressed()
        self.actor.saveLastPos()

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
