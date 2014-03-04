# -*-coding:utf-8-*-
import actors


class Monster(actors.Actor):
    def __init__(self, image, position, *groups):
        super(Monster, self).__init__(image, position, *groups)
