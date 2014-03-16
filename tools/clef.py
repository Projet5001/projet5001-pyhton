from basetool import BaseTool
from pygame import Rect


class Clef(BaseTool):
    def __init__(self, game, player, name, obj=None):
        super(Clef, self).__init__(game, player, name, obj)
        self.hub = self.__followPlayer__()
        self.rect = Rect((self.hub[0], self.hub[1]+8), (5, 100))
        self.image = None

    @classmethod
    def is_type_for(cls, object_type):
        return object_type == "clef"

    def handle_collision(self):
        self.player.ajoute_outils(self, self.game.layer_manager)
        self.tmx_object.visible = False
        self.visible = False

    def draw(self, screen):
        pass

    def update(self, dt, *args):
        pass

