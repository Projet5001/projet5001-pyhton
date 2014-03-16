
import os
import pygame
from lib import tmx


class LayerManager(object):

    def __init__(self, config, screen, clock):
        self.config = config
        self.screen = screen
        self.clock = clock
        self.tilemap = None
        self.layers = {}

    def __getitem__(self, key):
        try:
            return self.layers[key]
        except KeyError:
            return self.tilemap.layers[key]

    def remove(self, layer_name):
        if layer_name in self.layers:
            self.tilemap.layers.remove(layer_name)

    def set_map(self, game, new_map):
        print "set_map"
        map_path = os.path.join(self.config.get_asset_dir(), new_map)
        new_tilemap = tmx.load(map_path,
                               self.config.read_global('screen_size'))

        for layer in self.layers.keys():
            print layer
            new_tilemap.layers.add_named(self.layers[layer], layer)

        self.tilemap = new_tilemap


    def get_current_filename(self):
        return self.tilemap.filename

    def set_focus(self, px, py, boolean):
        for layer in self.tilemap.layers:
            print layer
        self.tilemap.set_focus(px, py, boolean)

    def update(self):
        dt = self.clock.tick()
        self.tilemap.update(dt, self)

    def draw(self, screen):
        self.screen.fill((0, 0, 0))
        self.tilemap.draw(screen)

    def new_layer(self, name, layer_type):
        layer = layer_type()
        self.add_layer(name, layer)

    def add_layer(self, name, layer):
        print name
        print layer
        self.tilemap.layers.add_named(layer, name)
        self.layers[name] = layer

