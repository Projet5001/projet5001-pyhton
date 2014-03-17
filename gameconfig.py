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
