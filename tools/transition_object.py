from pygame.locals import *
from basetool import BaseTool
import pygame


class TransitionObject(BaseTool):
    def __init__(self, game, player, name, obj=None):
        super(TransitionObject, self).__init__(game, player, name, obj)

    @classmethod
    def is_type_for(cls, object_type):
        allowed = ["porte", "escalier"]
        if object_type in allowed:
            return True
        return False

    def handle_collision(self):
        self.player.resetPos()
        self.game.effectuer_transition(self.tmx_object)

    def draw(self, screen):
        pass

    def update(self, dt, *args):
        pass

