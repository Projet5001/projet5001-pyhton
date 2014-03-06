# -*- coding: utf-8 -*-

from lib import tmx
class CollisionManager():

    def __init__(self, game):
        self.game = game

    #overide
    def spritecollideany(self, sprite, group, collided = None):
        if collided is None:
            for s in group:
                if sprite.rect.colliderect(s.collision_rect):
                    return s
        else:
            for s in group:
                if collided(sprite, s):
                    return s
        return None

    def player_stackEvents(self, sprit, groupe, playerEvents):

        coll = self.spritecollideany(sprit.tools[0], groupe)
        if coll:
            print 'collision'
            playerEvents.append(coll)

    def player_manageCollisionEvents(self, player, playerEvents):
        while len(playerEvents) > 0:
            e = playerEvents.pop()
            if e.block and e.attack:
                e.take_dommage(player.attack())
                print player.life

    def tmx_stackCollisionEvents(self, perso, tmxEvents):
        boundaries = self.game.tilemap.layers['boundaries']
        walls = self.game.tilemap.layers['walls']
        objets = None
        try:
            objets = self.game.tilemap.layers['objets']
        except KeyError:
            pass

        for cell in walls.collideLayer(perso.collision_rect):
            tmxEvents.append(cell)
        for cell in boundaries.collide(perso.collision_rect, 'block'):
            tmxEvents.append(cell)
        if objets:
            for objet in objets.collide(perso.collision_rect, 'type'):
                tmxEvents.append(objet)

    def tmx_manageCollisionEvents(self, perso, tmxEvents):
        while len(tmxEvents) > 0:
            e = tmxEvents.pop()

            try:
                if isinstance(e, tmx.Cell):
                    perso.resetPos()
                elif len(tmxEvents) == 0 and isinstance(e, tmx.Object):
                    if e.type == 'porte' or e.type == 'escalier':
                        perso.resetPos()
                        self.game.effectuer_transition(e)
                    else:
                        perso.objets.append(e.name)
                        e.visible = False

            except KeyError:
                # pas de clé block ici (e.g. pour un layer, où on ne peut pas
                # mettre de propriété à la cellule... :(
                perso.resetPos()
