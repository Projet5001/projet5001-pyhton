# -*- coding: utf-8 -*-
import pygame
from lib import tmx


class PlayerHud(tmx.Layer):
    def __init__(self, name, player, screen, tilemap):
        self.name = name
        self.visible = False
        self.player = player
        self.screen = screen
        self.tilemap = tilemap
        self.hud = {"x": 0, "y": 0}

    def setVisible(self, visible):
        self.visible = visible

    def __iter__(self):
        return tmx.LayerIterator(self)

    def update(self, dt, *args):
        self.hud = self.__findPlayer()

    def draw(self, surface):
        pygame.draw.line(surface,
                         (0, 0, 0),
                         (self.hud["x"], self.hud["y"]),
                         (self.hud["x"] + 1, self.hud["y"]),
                         1)
        self.__showName(surface)
        self.__showHealth(surface)

    def __showName(self, surface):
        myfont = pygame.font.SysFont("monospace", 15, True)
        label = myfont.render(self.player.name, 1, (255, 255, 255))
        surface.blit(label, (self.hud["x"] - (label.get_width() / 2),
                             self.hud["y"] - (self.tilemap.tile_height)))

    def __showHealth(self, surface):
        #line(Surface, color, start_pos, end_pos, width=1) -> Rect
        tileHalfWidth = self.tilemap.tile_width / 2
        origin_X = self.hud["x"] - tileHalfWidth
        origin_Y = self.hud["y"] - self.tilemap.tile_height / 2
        pygame.draw.line(surface,
                         (0, 0, 0),
                         (origin_X, origin_Y),
                         (origin_X + tileHalfWidth * 2, origin_Y),
                         5)
        health = (tileHalfWidth * 2) \
                    * float(self.player.health["hp"] \
                            / self.player.health["max"])
        pygame.draw.line(surface,
                         (255, 0, 0),
                         (origin_X, origin_Y),
                         (origin_X + health, origin_Y),
                         3)

    def __findPlayer(self):
        #Centrer la position du HUD par rapport au personnage
        player_X = self.player.collision_rect.x
        player_Y = self.player.collision_rect.y
        hud_X = player_X - (player_X - (self.screen.get_width() / 2))
        hud_Y = player_Y - (player_Y - (self.screen.get_height() / 2))
        #Gérer les bordures
        if(player_X < hud_X):
            hud_X = player_X
        if(player_Y < hud_Y):
            hud_Y = player_Y
        center_X = self.tilemap.px_width - self.screen.get_width() / 2
        center_Y = self.tilemap.px_height - self.screen.get_height() / 2
        if(player_X > center_X):
            hud_X += player_X - center_X
        if(player_Y > center_Y):
            hud_Y += player_Y - center_Y
        hud_X += self.tilemap.tile_width / 2
        hud_Y += self.tilemap.tile_height / 2
        return {"x": hud_X, "y": hud_Y - self.tilemap.tile_height}
