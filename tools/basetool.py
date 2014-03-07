# -*- coding: utf-8 -*-

import pygame
import importlib


class BaseTool(pygame.sprite.Sprite):
    def __init__(self, game, player, name, obj=None):
        super(BaseTool, self).__init__()
        self.game = game
        self.name = name
        self.player = player
        self.visible = False
        self.tmx_object = obj

    def is_equippable(self):
        return False

    def definir_position(self, x, y):
        pass

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

