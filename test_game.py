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

import unittest
from unittest import TestCase

from lib.tmx import Cell, Object

from main import Game
from player import Player
from monster import Monster


class MockGame(Game):
    def mainloop(self):
        pass


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = MockGame("test_etage_1.tmx")
        self.game.start()

    def tearDown(self):
        pass

    def __calcule_delta(self, player, destination):
        player_x = player.collision_rect.x
        player_y = player.collision_rect.y

        if isinstance(destination, Cell) \
                or isinstance(destination, Object):
            destination_x = destination.px
            destination_y = destination.py
        else:
            destination_x = destination.x
            destination_y = destination.y

        return (destination_x - player_x,
                destination_y - player_y)

    def test_charge_monstres(self):
        monstres = self.game.charge_monstres()
        TestCase.assertIn(self, monstres[0], self.game.monster_layer)

    def test_charge_player(self):
        player = self.game.charge_player()
        TestCase.assertIsInstance(self, player, Player)
        TestCase.assertEqual(self, player.name, "Max Power")

    def test_tmx_stackCollisionEvents(self):
        walls = self.game.tilemap.layers['walls']
        destination = walls.cells[walls.cells.keys()[0]]
        (dx, dy) = self.__calcule_delta(self.game.perso, destination)
        self.game.perso.move(dx, dy)
        TestCase.assertEqual(self, len(self.game.tmxEvents), 0)
        self.game.tmx_stackCollisionEvents(self.game.perso,
                                           self.game.tmxEvents)
        TestCase.assertGreater(self, len(self.game.tmxEvents), 0)

    def test_tmx_manageCollisionEvents(self):
        boundaries = self.game.tilemap.layers['boundaries']
        walls = self.game.tilemap.layers['walls']

        destination = walls.cells[walls.cells.keys()[0]]
        (dx, dy) = self.__calcule_delta(self.game.perso, destination)
        self.game.perso.move(dx, dy)
        TestCase.assertNotEquals(self,
                              self.game.perso.collision_rect.y,
                              self.game.perso.last_coll_y)
        self.game.tmx_stackCollisionEvents(self.game.perso,
                                           self.game.tmxEvents)
        self.game.tmx_manageCollisionEvents(self.game.perso,
                                            self.game.tmxEvents)
        TestCase.assertEquals(self,
                              self.game.perso.collision_rect.y,
                              self.game.perso.last_coll_y)

        destination = boundaries.find('destination')[0]
        dest_filename = destination.properties['destination']
        (dx, dy) = self.__calcule_delta(self.game.perso, destination)
        self.game.perso.move(dx, dy)
        self.game.tmx_stackCollisionEvents(self.game.perso,
                                           self.game.tmxEvents)
        self.game.tmx_manageCollisionEvents(self.game.perso,
                                            self.game.tmxEvents)
        TestCase.assertEquals(self,
                              self.game.tilemap.filename,
                              dest_filename)

    def test_effectuer_transition(self):
        dest = self.game.tilemap.layers['boundaries'].find('destination')[0]
        dest_filename = dest.properties['destination']
        self.game.effectuer_transition(dest)
        TestCase.assertEquals(self,
                              self.game.tilemap.filename,
                              dest_filename)

    def test_createHuds(self):
        # TODO: deleteHuds devrait retourner ce qu'il enleve pour simplifier
        # les tests.
        self.game.deleteHuds()
        #TestCase.assertNotIn(self,
        #                     self.game.tilemap.layers.by_name['playerHud'],
        #                     self.game.tilemap.layers)
        TestCase.assertNotIn(self,
                             'playerHud',
                             self.game.tilemap.layers.by_name)
        self.game.createHuds()
        TestCase.assertIn(self,
                          self.game.tilemap.layers.by_name['playerHud'],
                          self.game.tilemap.layers)
        TestCase.assertIn(self,
                          'playerHud',
                          self.game.tilemap.layers.by_name)

    def test_deleteHuds(self):
        TestCase.assertIn(self,
                          self.game.tilemap.layers.by_name['playerHud'],
                          self.game.tilemap.layers)
        TestCase.assertIn(self,
                          'playerHud',
                          self.game.tilemap.layers.by_name)

        # TODO: deleteHuds devrait retourner ce qu'il enleve pour simplifier
        # les tests.
        self.game.deleteHuds()

        TestCase.assertNotIn(self,
                             'playerHud',
                             self.game.tilemap.layers.by_name)

    def test_showHud(self):
        TestCase.assertFalse(self,
                             self.game.tilemap.layers['playerHud'].visible)
        self.game.showHud('playerHud')
        TestCase.assertTrue(self,
                            self.game.tilemap.layers['playerHud'].visible)

    def test_hideHud(self):
        self.game.showHud('playerHud')
        TestCase.assertTrue(self,
                            self.game.tilemap.layers['playerHud'].visible)
        self.game.hideHud('playerHud')
        TestCase.assertFalse(self,
                             self.game.tilemap.layers['playerHud'].visible)

    def test_addClockSec(self):
        self.game.addClockSec("playerHud", 1)
        TestCase.assertEquals(self,
                              self.game.clocks["playerHud"],
                              1 * self.game.FPS)

    def test_player_stackEvents(self):
        destination = self.game.tilemap.layers['pnjs'].find('monstre')[0]
        (dx, dy) = self.__calcule_delta(self.game.perso, destination)
        self.game.perso.move(dx, dy)
        self.game.player_stackEvents(self.game.perso,
                                     self.game.monster_layer,
                                     self.game.playerEvents)
        TestCase.assertGreater(self, len(self.game.playerEvents), 0)
        TestCase.assertIsInstance(self, self.game.playerEvents[0], Monster)

    def test_player_managerCollisionEvents(self):
        old_life = self.game.perso.life
        destination = self.game.tilemap.layers['pnjs'].find('monstre')[0]
        (dx, dy) = self.__calcule_delta(self.game.perso, destination)
        self.game.perso.move(dx, dy)
        self.game.player_stackEvents(self.game.perso,
                                     self.game.monster_layer,
                                     self.game.playerEvents)
        self.game.player_manageCollisionEvents(self.game.perso,
                                               self.game.playerEvents)
        TestCase.assertLess(self, self.game.perso.life, old_life)

if __name__ == "__main__":
    unittest.main()
