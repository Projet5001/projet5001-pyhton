# -*- coding: utf-8 -*-
from lib import tmx


class CollisionManager():

    def __init__(self, game):
        self.tmx = game.tilemap
        self.player = game.perso
        self.game = game
        self.player_groupe = self.tmx.layers['player_layer']
        self.monstre_groupe = self.tmx.layers['monster_layer']
        self.player_events = []
        self.tmx_events = []

    def set_tilemap(self, tilemap):
        self.tmx = tilemap

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

    def player_stackEvents(self):

        coll = self.spritecollideany()
        if coll:
            print 'collision'
            self.player_events.append(coll)

    def player_manageCollisionEvents(self):

        while len(self.player_events) > 0:
            e = self.player_events.pop()

            if e.block and e.attack:
                e.take_dommage(self.player.attack())
                print e.life

    def tmx_stackCollisionEvents(self):

        boundaries = self.tmx.layers['boundaries']
        walls = self.tmx.layers['walls']
        objets = None
        try:
            objets = self.game.tilemap.layers['objets']
        except KeyError:
            pass

        for cell in walls.collideLayer(self.player.collision_rect):
            self.tmx_events.append(cell)
        for cell in boundaries.collide(self.player.collision_rect, 'block'):
            self.tmx_events.append(cell)
        if objets:
            for objet in objets.collide(perso.collision_rect, 'type'):
                self.tmx_events.append(objet)

    def tmx_manageCollisionEvents(self):

        while len(self.tmx_events) > 0:
            e = self.tmx_events.pop()

            try:
                if isinstance(e, tmx.Cell):
                    self.player.resetPos()
                elif len(self.tmx_events) == 0 and isinstance(e, tmx.Object):
                    if e.type == 'porte' or e.type == 'escalier':
                        self.player.resetPos()
                        self.game.effectuer_transition(e)
                    else:
                        self.player.objets.append(e.name)
                        e.visible = False

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                self.player.resetPos()
