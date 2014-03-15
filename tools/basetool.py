# -*- coding: utf-8 -*-

from pygame import Rect, sprite
import importlib


class BaseTool(sprite.Sprite):
    def __init__(self, game, player, name, obj=None):
        super(BaseTool, self).__init__()
        self.game = game
        self.name = name
        self.player = player
        self.visible = False
        self.tmx_object = obj
        self.hub = None
        self.rect = Rect(0, 0, 0, 0)

    def is_equippable(self):
        return False

    def definir_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, *args):
        pass

    def handle_collision(self):
        pass

    def set_view(self, *args):
        pass

    @classmethod
    def make_tool(classe, game, player, tmx_object=None):
        classe.__load_subclasses()
        for tool_class in classe.__subclasses__():
            if tmx_object and tool_class.is_type_for(tmx_object.type):
                return tool_class(game, player, tmx_object.name, tmx_object)

    '''
    Import dynamically all the "subclasses" of Tool from the directory
    '''
    @classmethod
    def __load_subclasses(classe):
        try:
            import tools
        except ImportError:
            pass
        finally:
            for module in tools.__all__:
                importlib.import_module(".".join(["tools", module]))

    def __followPlayer__(self):
        #Centrer la position du HUD par rapport au personnage
        playerx, playery = self.player.collision_rect.x, self.player.collision_rect.y
        hubx = playerx - (playerx - (self.game.screen.get_width() / 2))
        huby = playery - (playery - (self.game.screen.get_height() / 2))

        if playerx < hubx:
            hubx = playerx

        if playery < huby:
            huby = playery

        centerx = self.game.tilemap.px_width - self.game.screen.get_width() / 2
        centery = self.game.tilemap.px_height - self.game.screen.get_height() / 2

        if playerx > centerx:
            hubx += playerx - centerx

        if playery > centery:
            huby += playery - centery
            hubx += self.game.tilemap.tile_width / 2
            huby += self.game.tilemap.tile_height / 2

        return hubx, huby
