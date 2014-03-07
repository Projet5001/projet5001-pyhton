from basetool import BaseTool
import pygame


class Clef(BaseTool):
    def __init__(self, game, player, name, obj=None):
        super(Clef, self).__init__(game, player, name, obj)

    @classmethod
    def is_type_for(cls, object_type):
        return object_type == "clef"

    def handle_collision(self):
        self.player.ajoute_outils(self)
        self.tmx_object.visible = False
        self.visible = False

    def draw(self, screen):
        pass

    def update(self, dt, *args):
        pass

