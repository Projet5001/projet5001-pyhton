# -*- coding: utf-8 -*-
from lib import tmx
from tools.basetool import BaseTool


class CollisionManager():

    def __init__(self, layer_manager):
        self.layer_manager = layer_manager
        self.player = None
        self.player_events = []
        self.tmx_events = []

        self.object_reference = {}

    def set_player(self, player):
        self.player = player

    #overide
    def spritecollideany(self, collided = None):
        try:
            for tool in self.player.tools.values():
                sprite = tool

                if collided is None:
                    for s in self.layer_manager['monster']:
                        if self.player.is_arme_active() and sprite.rect.colliderect(s.collision_rect):
                            print 'test'
                            return s
                else:
                    for s in self.monstre_groupe:
                        if collided(sprite, s):
                            return s
        except KeyError:
            pass

        return None

    def player_stackEvents(self):

        coll = self.spritecollideany()
        if coll:
            print 'collision'
            self.player_events.append(coll)

    def player_manageCollisionEvents(self):

        while len(self.player_events) > 0:
            e = self.player_events.pop()

            if e.block and e.attack:
                e.take_dommage(self.player.calcul_dommage())
                print e.life

    def tmx_stackCollisionEvents(self):

        boundaries = self.layer_manager['boundaries']
        walls = self.layer_manager['walls']
        objets = None
        try:
            objets = self.layer_manager['objets']
        except KeyError:
            pass

        for cell in walls.collideLayer(self.player.collision_rect):
            self.tmx_events.append(cell)
        for objet in boundaries.collide(self.player.collision_rect, 'block'):
            tool = None
            if objet not in self.object_reference:
                self.object_reference[objet] = \
                    BaseTool.make_tool(self.layer_manager, self.player, objet)
            else:
                tool = self.object_reference[objet]

            if tool:
                self.tmx_events.append(tool)

        if objets:
            for objet in objets.collide_any(self.player.collision_rect):
                tool = None

                if objet not in self.object_reference:
                    self.object_reference[objet] = \
                        BaseTool.make_tool(self.layer_manager, self.player, objet)
                else:
                    tool = self.object_reference[objet]

                if tool:
                    self.tmx_events.append(tool)

    def tmx_manageCollisionEvents(self):

        while len(self.tmx_events) > 0:
            e = self.tmx_events.pop()
            print e

            try:
                if isinstance(e, tmx.Cell):
                    self.player.resetPos()
                elif isinstance(e, BaseTool):
                    e.handle_collision()

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                self.player.resetPos()
