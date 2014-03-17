from pygame.locals import *
from basetool import BaseTool
import pygame


class TransitionObject(BaseTool):
    def __init__(self, layer_manager, player, name, obj=None):
        super(TransitionObject, self).__init__(layer_manager, player, name, obj)

    @classmethod
    def is_type_for(cls, object_type):
        allowed = ["porte", "escalier"]
        if object_type in allowed:
            return True
        return False

    def handle_collision(self):
        self.player.resetPos()

        # fire new event for transition (otherwise there is no way to call effectuer_transition)
        # TODO: rework events into own class.
        event = pygame.event.Event(pygame.USEREVENT+3, transition=self.tmx_object)
        pygame.event.post(event)

    def draw(self, screen):
        pass

    def update(self, dt, *args):
        pass

