# -*-coding:utf-8-*-
import actors


class Monster(actors.Actor):
    def __init__(self, name, image, position, *groups):
        super(Monster, self).__init__(name, image, position, *groups)

    def update(self, dt, game):
        pass
