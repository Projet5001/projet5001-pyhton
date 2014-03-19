
import os
import pygame
from operator import attrgetter, methodcaller
from lib import tmx


class LayerManager(object):

    def __init__(self, config, clock):
        self.config = config
        self.clock = clock

        self.screen = \
            pygame.display.set_mode(self.config.read_global("screen_size"))

        self.tilemap = None

        self.layers = {}
        self.attr_source = {
            "screen_height": ["screen", methodcaller('get_height')],
            "screen_width": ["screen", methodcaller('get_width')],
            "map_height": ["tilemap", attrgetter('px_height')],
            "map_width": ["tilemap", attrgetter('px_width')],
            "tile_height": ["tilemap", attrgetter('tile_height')],
            "tile_width": ["tilemap", attrgetter('tile_width')], }

    def __getattr__(self, name):
        if name in self.attr_source:
            obj = self.__getattribute__(self.attr_source[name][0])
            func = self.attr_source[name][1]
            return func(obj)
        else:
            return getattr(self.tilemap, name)

    def __getitem__(self, key):
        try:
            return self.layers[key]
        except KeyError:
            return self.tilemap.layers[key]

    def __contains__(self, key):
	return key in self.layers.keys()

    def remove(self, layer_name):
        if layer_name in self.layers:
            self.tilemap.layers.remove(self.layers[layer_name])
            del self.layers[layer_name]

    def set_map(self, game, new_map):
        map_path = os.path.join(self.config.get_asset_dir(), new_map)
        new_tilemap = tmx.load(map_path,
                               self.config.read_global('screen_size'))

        for layer in self.layers.keys():
            new_tilemap.layers.add_named(self.layers[layer], layer)

        self.tilemap = new_tilemap

    def get_current_filename(self):
        return self.tilemap.filename

    def set_focus(self, px, py, boolean):
        self.tilemap.set_focus(px, py, boolean)

    def update(self):
        dt = self.clock.tick()
        self.tilemap.update(dt, self)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.tilemap.draw(self.screen)

    def new_layer(self, name, layer_type):
        layer = layer_type()
        self.add_layer(name, layer)

    def add_layer(self, name, layer):
        self.tilemap.layers.add_named(layer, name)
        self.layers[name] = layer
