# -*- coding: utf-8 -*-
from lib import tmx


class CollisionManager():

    def __init__(self, player, tmx):
        self.tmx = tmx
        self.player = player
        self.player_groupe = self.tmx.layers['player_layer']
        self.monstre_groupe = self.tmx.layers['monster_layer']

    #overide
    def spritecollideany(self, collided = None):
        try:
            sprite = self.player.tools[0]

            if collided is None:
                        for s in self.monstre_groupe:
                            if sprite.rect.colliderect(s.collision_rect):
                                return s
            else:
                for s in self.monstre_groupe:
                    if collided(sprite, s):
                        return s
        except KeyError:
            pass

        return None

    def player_stackEvents(self, player_events):

        coll = self.spritecollideany()
        if coll:
            print 'collision'
            player_events.append(coll)

    def player_manageCollisionEvents(self, player_events):

        while len(player_events) > 0:
            e = player_events.pop()

            if e.block and e.attack:
                e.take_dommage(self.player.attack())
                print e.life

    def tmx_stackCollisionEvents(self,tmxEvents):

        boundaries = self.tmx.layers['boundaries']
        walls = self.tmx.layers['walls']
        for cell in walls.collideLayer(self.player.collision_rect):
            tmxEvents.append(cell)
        for cell in boundaries.collide(self.player.collision_rect, 'block'):
            tmxEvents.append(cell)

    def tmx_manageCollisionEvents(self, tmx_events):

        while len(tmx_events) > 0:
            e = tmx_events.pop()

            try:
                if isinstance(e, tmx.Cell):
                    self.player.resetPos()
                elif len(tmx_events) == 0 and isinstance(e, tmx.Object):
                    self.player.resetPos()
                    #self.game.effectuer_transition(e)

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                self.player.resetPos()
