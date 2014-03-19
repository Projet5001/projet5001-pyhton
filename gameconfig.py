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
import json


class GameConfig():
    def __init__(self, conffile):
        self.config_file = open(conffile, "r")
        self.base_path = os.path.dirname(conffile)
        self.config = json.load(self.config_file)

    def get_asset_dir(self):
        return os.path.join(self.base_path, self.read_global('asset_dir'))

    def get_sprite_dir(self):
        return os.path.join(self.base_path, self.read_global('sprite_dir'))

    def get_tileset_dir(self):
        return os.path.join(self.base_path, self.read_global('tileset_dir'))

    def get_start_map(self):
        return self.read_global('start_map')

    def read_global(self, key):
        return self.config['global'][key]

    def read(self, map_key, key):
        return self.config[map_key][key]
