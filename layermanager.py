# -*- coding: utf-8 -*-
#
# Projet5001: un jeu de survie post-apocalyptique
# Copyright (C) 2014  Équipe Projet5001
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
from operator import attrgetter, methodcaller

import pygame

from lib import tmx


class LayerManager(object):

    def __init__(self, config, clock):
        self.config = config
        self.clock = clock

        self.screen = \
            pygame.display.set_mode(self.config.read_global("screen_size"))

        self.tilemap = None

        self.blocking = False

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

        # Empty the monster and NPC layers.
        if "monster" in self.layers:
            self.layers["monster"].empty()
        if "npcs" in self.layers:
            self.layers["npcs"].empty()

        for layer in self.layers.keys():
            if layer == "player":
                player_stack_index = new_tilemap.layers.index(new_tilemap.layers['hint'])
                new_tilemap.layers.insert_named(player_stack_index, self.layers[layer], layer)
            elif "hidden" not in layer:
                new_tilemap.layers.add_named(self.layers[layer], layer)

        self.tilemap = new_tilemap

    def find_layer(self, lam):
        layers = []
        for layer in self.layers:
            if lam(self.layers[layer]):
                layers.append(self.layers[layer])
        return layers

    def get_sprite(self, name):
        x = lambda y: isinstance(y, tmx.SpriteLayer)
        layers = self.find_layer(x)
        for layer in layers:
            sprites = layer.sprites()
            for spr in sprites:
                if spr.name == name:
                    return spr

    def get_current_filename(self):
        return self.tilemap.filename

    def set_focus(self, px, py, boolean):
        self.tilemap.set_focus(px, py, boolean)

    def update(self, blocking):
        self.blocking = blocking
        dt = self.clock.tick()
        self.tilemap.update(dt, self)

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.tilemap.draw(self.screen)

    def new_layer(self, name, layer_type):
        layer = layer_type()
        self.add_layer(name, layer)

    def add_layer(self, name, layer):
        if name == "player":
            player_stack_index = self.tilemap.layers.index(self.tilemap.layers['hint'])
            self.tilemap.layers.insert_named(player_stack_index, layer, name)
        else:
            self.tilemap.layers.add_named(layer, name)
        self.layers[name] = layer

