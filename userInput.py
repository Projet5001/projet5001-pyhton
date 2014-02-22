import pygame


class Keyboard():
    def __init__(self, perso):
        self.perso = perso
        self.speed = perso.speed
        self.accel = perso.accel

    def move_left(self):
        self.perso.move(-(self.speed * self.accel), 0)

    def move_right(self):
        self.perso.move((self.speed * self.accel), 0)

    def move_up(self):
        self.perso.move(0, -(self.speed * self.accel))

    def move_down(self):
        self.perso.move(0, (self.speed * self.accel))

    def jump(self):
        pass

    def updateKey(self, dt):
        pressedkeys = pygame.key.get_pressed()
        self.perso.saveLastPos()

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
