#-*-coding:utf-8-*-
'''
Created on 2014-02-18

@author: mtrudel
'''

import unittest
from unittest import TestCase
from actors import Actor


class ActorTest(TestCase):

    group = []

    def setUp(self):
        self.actor = Actor("../assets/sprites/perso.png", (0, 0), self.group)

    def testActorMoveChangeRect(self):
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

    def testActorMoveChangeCollisionRect(self):
        TestCase.assertEqual(self,
                             self.actor.collision_rect.x,
                             0)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.y,
                             20)
        self.actor.move(1, 1)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.x,
                             1)
        TestCase.assertEqual(self,
                             self.actor.collision_rect.y,
                             21)

if __name__ == "__main__":
    unittest.main()
