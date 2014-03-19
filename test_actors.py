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

from actors import Actor


class ActorTest(TestCase):

    group = []

    def setUp(self):
        self.actor = Actor("assets/sprites/perso.png", (0, 0), self.group)

    def test_move_changes_actor_rect(self):
        TestCase.assertEqual(self,
                             self.actor.rect.x,
                             0)
        TestCase.assertEqual(self,
                             self.actor.rect.y,
                             0)
        self.actor.move(1, 1)
        TestCase.assertEqual(self,
                             self.actor.rect.x,
                             1)
        TestCase.assertEqual(self,
                             self.actor.rect.y,
                             1)

    def test_move_changes_collision_rect(self):
        TestCase.assertEqual(self,
                             self.actor.collision_rect.x,
                             2)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.y,
                             30)
        self.actor.move(1, 1)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.x,
                             3)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.y,
                             31)

    def test_save_x_pos(self):
        old_last_x = self.actor.last_x
        old_last_y = self.actor.last_y
        self.actor.move(1, 1)
        self.actor.save_x_pos()
        TestCase.assertNotEqual(self, old_last_x, self.actor.last_x)
        TestCase.assertEqual(self, old_last_y, self.actor.last_y)

    def test_save_y_pos(self):
        old_last_x = self.actor.last_x
        old_last_y = self.actor.last_y
        self.actor.move(1, 1)
        self.actor.save_y_pos()
        TestCase.assertEqual(self, old_last_x, self.actor.last_x)
        TestCase.assertNotEqual(self, old_last_y, self.actor.last_y)

    def test_reset_x(self):
        old_x = self.actor.last_coll_x
        self.actor.move(100, 100)
        TestCase.assertNotEqual(self, old_x, self.actor.collision_rect.x)
        self.actor.resetPos()
        TestCase.assertEqual(self, old_x, self.actor.last_coll_x)

    def test_reset_y(self):
        old_y = self.actor.last_coll_y
        self.actor.move(0, 100)
        TestCase.assertNotEqual(self, old_y, self.actor.collision_rect.y)
        self.actor.resetPos()
        TestCase.assertEqual(self, old_y, self.actor.last_coll_y)

    def test_definir_position(self):
        self.actor.definir_position(150, 250)
        TestCase.assertEqual(self, self.actor.collision_rect.x, 150)
        TestCase.assertEqual(self, self.actor.collision_rect.y, 250)

    def test_attack(self):
        TestCase.assertEqual(self,
                             self.actor.attack(),
                             self.actor.dommage
                             * self.actor.luck())

    def test_take_dommage(self):
        life = self.actor.life
        protection = self.actor.protectionTotal()
        dommage = protection + 10
        self.actor.take_dommage(dommage)
        TestCase.assertEqual(self, self.actor.life, life - dommage)

    @unittest.skip("non-implemente dans la classe")
    def test_block(self):
        pass

    @unittest.skip("non-implemente dans la classe")
    def test_luck(self):
        pass

    def test_protectionTotal(self):
        TestCase.assertEqual(self,
                             self.actor.protectionTotal(),
                             self.actor.protection)

    def test_isBleeding(self):
        self.actor.life = 0
        TestCase.assertNotIn(self, self.actor, self.actor.groups())

if __name__ == "__main__":
    unittest.main()
