# -*- coding: utf-8 -*-
import pygame
from lib import tmx


class PlayerHud(tmx.Layer):
    def __init__(self, name, player, layer_manager):

        self.name = name
        self.visible = True
        self.player = player
        self.layer_manager = layer_manager

    def move(self, offsetx, offsety):
        pass

    def setVisible(self, visible):
        self.visible = visible

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        pass

    def draw(self, surface):
        # Tous les autres objets seront placés en relation avec ce point
        hub = self.__followPlayer()
        pygame.draw.line(surface,
                         (0, 0, 0),
                         (hub["x"], hub["y"]),
                         (hub["x"] + 1, hub["y"]),
                         1)
        hub["y"] -= self.layer_manager.tile_height
        self.__showName(surface, (hub["x"], hub["y"]))
        self.__showHealth(surface, (hub["x"], hub["y"] + 5))

    def __showName(self, surface, hub):
        myfont = pygame.font.SysFont("monospace", 15, True)
        label = myfont.render(self.player.name, 1, (255, 255, 255))
        surface.blit(label, (hub[0] - (label.get_width() / 2),
                             hub[1] - (self.layer_manager.tile_height)))

    def __showHealth(self, surface, hub):
        #line(Surface, color, start_pos, end_pos, width=1) -> Rect
        tileHalfWidth = self.layer_manager.tile_width / 2
        originx = hub[0] - tileHalfWidth
        originy = hub[1] - self.layer_manager.tile_height / 2
        pygame.draw.line(surface,
                         (0, 0, 0),
                         (originx, originy),
                         (originx + tileHalfWidth * 2, originy),
                         5)
        health = (tileHalfWidth * 2) \
                    * float(self.player.health["hp"] \
                            / self.player.health["max"])
        pygame.draw.line(surface,
                         (255, 0, 0),
                         (originx, originy),
                         (originx + health, originy),
                         3)

    def __followPlayer(self):
        #Centrer la position du HUD par rapport au personnage
        playerx = self.player.collision_rect.x
        playery = self.player.collision_rect.y
        hubx = playerx - (playerx - (self.layer_manager.screen_width / 2))
        huby = playery - (playery - (self.layer_manager.screen_height / 2))
        #Gérer les bordures
        if(playerx < hubx):
            hubx = playerx
        if(playery < huby):
            huby = playery
        centerx = \
            self.layer_manager.map_width - self.layer_manager.screen_width / 2
        centery = \
            self.layer_manager.map_height - self.layer_manager.screen_height / 2
        if(playerx > centerx):
            hubx += playerx - centerx
        if(playery > centery):
            huby += playery - centery
        hubx += self.layer_manager.tile_width / 2
        huby += self.layer_manager.tile_height / 2
        return {"x": hubx, "y": huby}
